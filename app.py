import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy import create_engine, desc, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Meeting, Transcript, Attendee

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure CORS based on environment setting
if os.environ.get('ALLOW_CORS', 'false').lower() == 'true':
    CORS(app)

# Database setup
DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create data directory if it doesn't exist (for backward compatibility)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                        os.environ.get('DATA_DIR', 'data'))
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def parse_datetime(datetime_str):
    """Parse datetime string to datetime object"""
    try:
        return datetime.strptime(datetime_str, "%m/%d/%Y, %I:%M:%S %p")
    except ValueError:
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.now()

@app.route('/api/transcripts', methods=['POST'])
def save_transcript():
    data = request.json
    
    # Basic validation
    if not data or 'meetingId' not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    meeting_id = data.get('meetingId')
    meeting_title = data.get('meetingTitle', 'Unnamed Meeting')
    meeting_unique_id = data.get('meetingUniqueId', f"{meeting_title}_{datetime.now().strftime('%Y-%m-%d')}")
    
    # Check if meeting exists
    meeting = db_session.query(Meeting).filter_by(meeting_unique_id=meeting_unique_id).first()
    
    if not meeting:
        # Create new meeting if it doesn't exist
        meeting = Meeting(
            meeting_id=meeting_id,
            meeting_unique_id=meeting_unique_id,
            meeting_title=meeting_title,
            meeting_start_time=parse_datetime(data.get('meetingStartTime', datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")))
        )
        db_session.add(meeting)
        db_session.commit()
    
    # Handle both legacy format (transcript field) and new format (transcriptSegments array)
    if 'transcriptSegments' in data and isinstance(data['transcriptSegments'], list):
        # New format: individual segments
        for segment in data['transcriptSegments']:
            transcript = Transcript(
                meeting_id=meeting.id,
                text=segment.get('text', ''),
                speaker=segment.get('speaker', 'Unknown'),
                user_email=data.get('userEmail', ''),
                timestamp=parse_datetime(segment.get('timestamp', datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")))
            )
            db_session.add(transcript)
    elif 'transcript' in data:
        # Legacy format: single transcript text
        transcript = Transcript(
            meeting_id=meeting.id,
            text=data.get('transcript', ''),
            speaker=data.get('speaker', 'Unknown'),
            user_email=data.get('userEmail', ''),
            timestamp=parse_datetime(data.get('timestamp', datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")))
        )
        db_session.add(transcript)
    else:
        # No transcript data provided
        return jsonify({"error": "No transcript data provided"}), 400
    
    db_session.commit()
    
    # Update attendees if provided
    if 'attendees' in data and isinstance(data['attendees'], list):
        for attendee_data in data['attendees']:
            participant_id = attendee_data.get('id')
            
            # Skip if no participant ID
            if not participant_id:
                continue
                
            # Check if attendee already exists
            existing_attendee = db_session.query(Attendee).filter_by(
                meeting_id=meeting.id, 
                participant_id=participant_id
            ).first()
            
            if not existing_attendee:
                # Add new attendee
                attendee = Attendee(
                    meeting_id=meeting.id,
                    participant_id=participant_id,
                    name=attendee_data.get('name', 'Unknown'),
                    email=attendee_data.get('email', ''),
                    join_time=parse_datetime(attendee_data.get('joinTime', datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")))
                )
                db_session.add(attendee)
        
        db_session.commit()
    
    return jsonify({"status": "success", "message": "Transcript saved successfully"}), 200

@app.route('/api/attendees', methods=['POST'])
def save_attendee():
    data = request.json
    
    # Basic validation
    if not data or 'meetingId' not in data or 'attendee' not in data:
        return jsonify({"error": "Invalid data format"}), 400
    
    meeting_id = data.get('meetingId')
    meeting_title = data.get('meetingTitle', 'Unnamed Meeting')
    meeting_unique_id = data.get('meetingUniqueId', f"{meeting_title}_{datetime.now().strftime('%Y-%m-%d')}")
    
    # Check if meeting exists
    meeting = db_session.query(Meeting).filter_by(meeting_unique_id=meeting_unique_id).first()
    
    if not meeting:
        # Create new meeting if it doesn't exist
        meeting = Meeting(
            meeting_id=meeting_id,
            meeting_unique_id=meeting_unique_id,
            meeting_title=meeting_title,
            meeting_start_time=parse_datetime(data.get('meetingStartTime', datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")))
        )
        db_session.add(meeting)
        db_session.commit()
    
    # Add or update attendee
    attendee_data = data.get('attendee', {})
    
    # Support both participant_id (new format) and id (legacy format)
    participant_id = None
    if 'participant_id' in attendee_data:
        participant_id = attendee_data.get('participant_id')
    else:
        participant_id = attendee_data.get('id')
    
    if not participant_id:
        return jsonify({"error": "Attendee ID is required"}), 400
    
    # Check if attendee already exists
    existing_attendee = db_session.query(Attendee).filter_by(
        meeting_id=meeting.id, 
        participant_id=participant_id
    ).first()
    
    if existing_attendee:
        # Update existing attendee
        existing_attendee.name = attendee_data.get('name', existing_attendee.name)
        existing_attendee.email = attendee_data.get('email', existing_attendee.email)
    else:
        # Add new attendee
        # Support both join_time (new format) and joinTime (legacy format)
        join_time = None
        if 'join_time' in attendee_data:
            join_time = attendee_data.get('join_time')
        else:
            join_time = attendee_data.get('joinTime')
            
        attendee = Attendee(
            meeting_id=meeting.id,
            participant_id=participant_id,
            name=attendee_data.get('name', 'Unknown'),
            email=attendee_data.get('email', ''),
            join_time=parse_datetime(join_time or datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"))
        )
        db_session.add(attendee)
    
    db_session.commit()
    
    return jsonify({"status": "success", "message": "Attendee saved successfully"}), 200

@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    # Query all meetings, ordered by update time (newest first)
    meetings = db_session.query(Meeting).order_by(desc(Meeting.updated_at)).all()
    
    # Convert to dict for JSON response
    meetings_list = [meeting.to_dict() for meeting in meetings]
    
    return jsonify(meetings_list), 200

@app.route('/api/meetings/<meeting_unique_id>', methods=['GET'])
def get_meeting_details(meeting_unique_id):
    # Query the meeting
    meeting = db_session.query(Meeting).filter_by(meeting_unique_id=meeting_unique_id).first()
    
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    
    # Query transcripts for this meeting
    transcripts = db_session.query(Transcript).filter_by(meeting_id=meeting.id).order_by(Transcript.timestamp).all()
    
    # Query attendees for this meeting
    attendees = db_session.query(Attendee).filter_by(meeting_id=meeting.id).all()
    
    # Format the response
    attendees_dict = {attendee.participant_id: attendee.to_dict() for attendee in attendees}
    
    result = {
        "meeting": meeting.to_dict(),
        "transcripts": [transcript.to_dict() for transcript in transcripts],
        "attendees": attendees_dict
    }
    
    return jsonify(result), 200

@app.route('/', methods=['GET'])
def index():
    """
    Render the main HTML interface
    """
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring the API status"""
    try:
        # Check database connection
        db_session.execute(text("SELECT 1"))
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "version": "1.0.0",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    debug = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug) 
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Meeting(Base):
    """Meeting model representing a Google Meet session"""
    __tablename__ = 'meetings'

    id = Column(Integer, primary_key=True)
    meeting_id = Column(String(255), nullable=False)
    meeting_unique_id = Column(String(255), nullable=False, unique=True)
    meeting_title = Column(String(255), nullable=False)
    meeting_start_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transcripts = relationship("Transcript", back_populates="meeting", cascade="all, delete-orphan")
    attendees = relationship("Attendee", back_populates="meeting", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "meetingId": self.meeting_id,
            "meetingUniqueId": self.meeting_unique_id,
            "meetingTitle": self.meeting_title,
            "meetingStartTime": self.meeting_start_time.strftime("%m/%d/%Y, %I:%M:%S %p"),
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "hasTranscript": len(self.transcripts) > 0,
            "hasAttendees": len(self.attendees) > 0,
            "lastUpdated": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

class Transcript(Base):
    """Transcript model for storing transcript segments"""
    __tablename__ = 'transcripts'

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    text = Column(Text, nullable=False)
    speaker = Column(String(255))
    user_email = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    meeting = relationship("Meeting", back_populates="transcripts")
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "speaker": self.speaker,
            "userEmail": self.user_email,
            "timestamp": self.timestamp.strftime("%m/%d/%Y, %I:%M:%S %p"),
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

class Attendee(Base):
    """Attendee model for tracking meeting participants"""
    __tablename__ = 'attendees'

    id = Column(Integer, primary_key=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id'), nullable=False)
    participant_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    join_time = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    meeting = relationship("Meeting", back_populates="attendees")
    
    def to_dict(self):
        return {
            "id": self.id,
            "participantId": self.participant_id,
            "name": self.name,
            "email": self.email,
            "joinTime": self.join_time.strftime("%m/%d/%Y, %I:%M:%S %p"),
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } 
"""
Test cases for the Flask API endpoints.
"""
import json
import os
from datetime import datetime

def test_health_endpoint(client):
    """Test the health endpoint returns the correct response."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'database' in data
    assert 'version' in data
    assert 'timestamp' in data

def test_get_meetings(client):
    """Test the meetings endpoint returns a list of meetings."""
    response = client.get('/api/meetings')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_save_transcript(client):
    """Test saving a transcript."""
    data = {
        "meetingId": "test-meeting-id",
        "meetingTitle": "Test Meeting",
        "meetingUniqueId": f"Test Meeting_{datetime.now().strftime('%m-%d-%Y')}",
        "meetingStartTime": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
        "userEmail": "test@example.com",
        "timestamp": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
        "transcriptSegments": [
            {
                "timestamp": "10:05:30",
                "speaker": "Test User",
                "text": "This is a test transcript."
            }
        ],
        "attendees": [
            {
                "participant_id": "test-user-1",
                "name": "Test User",
                "email": "test@example.com",
                "join_time": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
            }
        ]
    }
    
    response = client.post(
        '/api/transcripts',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 'success'
    assert result['message'] == 'Transcript saved successfully'

def test_save_attendee(client):
    """Test saving an attendee."""
    data = {
        "meetingId": "test-meeting-id",
        "meetingTitle": "Test Meeting",
        "meetingUniqueId": f"Test Meeting_{datetime.now().strftime('%m-%d-%Y')}",
        "meetingStartTime": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
        "timestamp": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p"),
        "userEmail": "test@example.com",
        "attendee": {
            "participant_id": "test-user-2",
            "name": "Another Test User",
            "email": "another@example.com",
            "join_time": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
        }
    }
    
    response = client.post(
        '/api/attendees',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 'success'
    assert result['message'] == 'Attendee saved successfully' 
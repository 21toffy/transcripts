# Google Meet Transcription API

A Flask API server that receives and stores transcription data from the Google Meet Transcriber Add-on using PostgreSQL.

## Features

- Receives and stores transcripts from Google Meet Add-on
- Tracks meeting attendees
- Stores data in PostgreSQL database
- Provides simple API endpoints for data access
- Web interface for reviewing past meeting transcripts

## Installation

### Requirements

- Python 3.7+
- Flask
- PostgreSQL database (we use Supabase)
- SQLAlchemy

### Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables (copy `.env.example` to `.env` and edit):
   ```
   cp .env.example .env
   # Edit .env to include your DATABASE_URL
   ```
4. Initialize the database:
   ```
   python init_db.py
   ```
5. Run the server:
   ```
   python app.py
   ```

## Database Schema

The application uses a PostgreSQL database with the following tables:

- **meetings**: Stores meeting metadata
- **transcripts**: Stores transcript segments
- **attendees**: Stores information about meeting participants

The schema is defined in `schema.sql` and is managed using SQLAlchemy ORM.

## API Endpoints

### `POST /api/transcripts`

Receives transcript data from the Google Meet Add-on.

**Request body example:**
```json
{
  "meetingId": "abc-def-ghi",
  "meetingTitle": "Team Meeting",
  "meetingUniqueId": "Team_Meeting_06-15-2023",
  "meetingStartTime": "6/15/2023, 2:30:00 PM",
  "userEmail": "user@example.com",
  "timestamp": "6/15/2023, 2:35:00 PM",
  "transcript": "[2:31:30 PM] John: Hello everyone\n[2:31:35 PM] Mary: Hi John",
  "attendees": [
    {
      "id": "user1",
      "name": "John Doe",
      "joinTime": "6/15/2023, 2:30:00 PM"
    },
    {
      "id": "user2",
      "name": "Mary Smith",
      "joinTime": "6/15/2023, 2:30:30 PM"
    }
  ]
}
```

### `POST /api/attendees`

Receives notifications about new attendees joining the meeting.

**Request body example:**
```json
{
  "event": "new_attendee",
  "meetingId": "abc-def-ghi",
  "meetingTitle": "Team Meeting",
  "meetingUniqueId": "Team_Meeting_06-15-2023",
  "timestamp": "6/15/2023, 2:35:00 PM",
  "userEmail": "host@example.com",
  "attendee": {
    "id": "user3",
    "name": "Bob Johnson",
    "joinTime": "6/15/2023, 2:35:00 PM"
  }
}
```

### `GET /api/meetings`

Lists all recorded meetings.

### `GET /api/meetings/<meeting_unique_id>`

Gets detailed information about a specific meeting.

## Deployment

### Using Docker

Build and run the Docker container:

```bash
docker build -t meet-transcriber-api .
docker run -p 5005:5005 -e DATABASE_URL=your_database_url meet-transcriber-api
```

### Using Docker Compose

```bash
docker-compose up -d
```

## Supabase Integration

This application is configured to use Supabase PostgreSQL. To connect to your Supabase database:

1. Get your connection string from Supabase dashboard
2. Set the `DATABASE_URL` environment variable in your `.env` file:
   ```
   DATABASE_URL=postgresql://postgres:password@db.yourproject.supabase.co:5432/postgres
   ```
3. Initialize the database using `init_db.py`

## Using with Google Meet Add-on

When deploying this backend, make sure to:

1. Use a public URL that's accessible from the internet
2. Configure CORS if needed (already enabled in the code)
3. Set the backend URL in the Google Meet Add-on

Example URL to use in the Meet Add-on:
```
https://your-deployed-app.example.com/api/transcripts
``` # transcripts

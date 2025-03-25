-- Initialize the database schema

-- Meetings table
CREATE TABLE IF NOT EXISTS meetings (
    id SERIAL PRIMARY KEY,
    meeting_id VARCHAR(255) NOT NULL,
    meeting_unique_id VARCHAR(255) NOT NULL UNIQUE,
    meeting_title VARCHAR(255) NOT NULL,
    meeting_start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Transcripts table
CREATE TABLE IF NOT EXISTS transcripts (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    speaker VARCHAR(255),
    user_email VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendees table
CREATE TABLE IF NOT EXISTS attendees (
    id SERIAL PRIMARY KEY,
    meeting_id INTEGER NOT NULL REFERENCES meetings(id) ON DELETE CASCADE,
    participant_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    join_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (meeting_id, participant_id)
);

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_meeting_unique_id ON meetings(meeting_unique_id);
CREATE INDEX IF NOT EXISTS idx_transcripts_meeting_id ON transcripts(meeting_id);
CREATE INDEX IF NOT EXISTS idx_attendees_meeting_id ON attendees(meeting_id);
CREATE INDEX IF NOT EXISTS idx_transcripts_timestamp ON transcripts(timestamp);
CREATE INDEX IF NOT EXISTS idx_attendees_join_time ON attendees(join_time); 
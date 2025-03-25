#!/bin/bash

# Load environment variables from .env file
set -a
source .env
set +a

echo "Starting Google Meet Transcription API"
echo "======================================="

# Check if database initialization is needed
echo "Checking database connection and initializing if needed..."
python init_db.py

# Start the Flask application
echo "Starting Flask application..."
if [ "$FLASK_ENV" = "development" ]; then
  # Run in development mode with debug
  flask run --host=0.0.0.0
else
  # Run in production mode with gunicorn
  gunicorn --workers=2 --bind=0.0.0.0:${PORT:-5005} app:app
fi 
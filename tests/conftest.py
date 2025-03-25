"""
Configuration file for pytest.
"""
import os
import sys
import pytest
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables from .env file
load_dotenv()

# Import the Flask app
from app import app as flask_app
from app import db_session

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Set testing configuration
    flask_app.config.update({
        "TESTING": True,
    })
    
    # Return the app for testing
    yield flask_app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture(autouse=True)
def session():
    """Provide a database session for each test."""
    # Setup: start a new database session
    yield db_session
    
    # Teardown: close the session after each test
    db_session.remove() 
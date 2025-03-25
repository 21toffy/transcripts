#!/usr/bin/env python
"""
Script to set up and tear down the test database.
"""
import os
import sys
from dotenv import load_dotenv

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load test environment variables
load_dotenv('.env.test')

from models import Base
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get('DATABASE_URL')

def setup_test_db():
    """Create all tables in the test database."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Test database set up successfully.")

def teardown_test_db():
    """Drop all tables from the test database."""
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    print("Test database torn down successfully.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teardown":
        teardown_test_db()
    else:
        setup_test_db() 
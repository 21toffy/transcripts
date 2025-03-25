#!/usr/bin/env python3
"""Initialize the database tables if they don't exist"""

import os
import sys
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

def main():
    """Main function to create database tables"""
    # Get database URL from environment
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("Error: DATABASE_URL environment variable not set")
        sys.exit(1)
        
    # Connect to the database
    try:
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        print("Connected to database successfully")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)
    
    # Read the SQL schema
    try:
        with open('schema.sql', 'r') as f:
            sql = f.read()
    except Exception as e:
        print(f"Error reading schema.sql: {e}")
        sys.exit(1)
    
    # Execute the SQL
    try:
        cursor.execute(sql)
        print("Database schema created successfully")
    except Exception as e:
        print(f"Error creating database schema: {e}")
        sys.exit(1)
    
    # Close the connection
    cursor.close()
    conn.close()
    print("Database initialized successfully")

if __name__ == "__main__":
    main() 
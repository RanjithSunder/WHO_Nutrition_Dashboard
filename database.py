import sqlite3
import os
import pandas as pd
from datetime import datetime

DATABASE_PATH = "who_nutrition_data.db"
DATA_TIMESTAMP_KEY = "data_timestamp"

def check_database_exists():
    """Check if database file exists and is valid"""
    return os.path.exists(DATABASE_PATH) and os.path.getsize(DATABASE_PATH) > 0

def get_database_info():
    """Get information about the existing database"""
    if not check_database_exists():
        return None

    try:
        conn = sqlite3.connect(DATABASE_PATH)

        # Check if tables exist
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        if 'obesity' not in tables or 'malnutrition' not in tables:
            conn.close()
            return None

        # Get record counts
        obesity_count = pd.read_sql_query("SELECT COUNT(*) as count FROM obesity", conn).iloc[0]['count']
        malnutrition_count = pd.read_sql_query("SELECT COUNT(*) as count FROM malnutrition", conn).iloc[0]['count']

        # Get data timestamp if exists
        try:
            timestamp_query = "SELECT value FROM metadata WHERE key = ?"
            timestamp_result = pd.read_sql_query(timestamp_query, conn, params=(DATA_TIMESTAMP_KEY,))
            if len(timestamp_result) > 0:
                data_timestamp = timestamp_result.iloc[0]['value']
            else:
                data_timestamp = "Unknown"
        except:
            data_timestamp = "Unknown"

        conn.close()

        return {
            'obesity_count': obesity_count,
            'malnutrition_count': malnutrition_count,
            'timestamp': data_timestamp,
            'file_size': f"{os.path.getsize(DATABASE_PATH) / (1024 * 1024):.2f} MB"
        }

    except Exception as e:
        st.error(f"Error reading database: {e}")
        return None

def create_metadata_table(conn):
    """Create metadata table to store processing information"""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

def save_data_timestamp(conn):
    """Save the timestamp when data was last processed"""
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO metadata (key, value, created_at) 
        VALUES (?, ?, ?)
    ''', (DATA_TIMESTAMP_KEY, datetime.now().isoformat(), datetime.now()))
    conn.commit()

def load_from_database():
    """Load data from existing database"""
    conn = sqlite3.connect(DATABASE_PATH)

    try:
        df_obesity = pd.read_sql_query("SELECT * FROM obesity", conn)
        df_malnutrition = pd.read_sql_query("SELECT * FROM malnutrition", conn)
        return df_obesity, df_malnutrition, conn
    except Exception as e:
        st.error(f"Error loading from database: {e}")
        conn.close()
        return None, None, None

def create_persistent_database(df_obesity, df_malnutrition):
    """Create persistent SQLite database"""
    conn = sqlite3.connect(DATABASE_PATH)

    # Create metadata table
    create_metadata_table(conn)

    # Create tables and insert data
    df_obesity.to_sql('obesity', conn, if_exists='replace', index=False)
    df_malnutrition.to_sql('malnutrition', conn, if_exists='replace', index=False)

    # Save timestamp
    save_data_timestamp(conn)

    conn.close()
    return sqlite3.connect(DATABASE_PATH)
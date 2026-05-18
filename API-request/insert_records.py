import os
import psycopg2
from api_request import mock_fetch_data

def connect_to_db():
    print("Connecting to the Postgresql database...")
    try: 
        conn = psycopg2.connect(
            host="localhost",
            port=5000,
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"]
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise


def create_table(conn):
    print("Creating table if not exist...")

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY, 
                city TEXT,
                temperature FLOAT,
                weather_descriptions TEXT, 
                wind_speed FLOAT,
                time TIMESTAMP, 
                inserted_at TIMESTAMP DEFAULT NOW(), 
                utc_offset TEXT  
            );
        """)
        conn.commit()
        print("Table was created.")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise

conn = connect_to_db()
create_table(conn)


# def insert_records(conn, data):
#     print("Inserting weather data into the database...")
#     try: 
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO dev.raw_weather_data(
#                 city TEXT,
#                 temperature FLOAT,
#                 weather_descriptions TEXT, 
#                 wind_speed FLOAT,
#                 time TIMESTAMP, 
#                 inserted_at TIMESTAMP DEFAULT NOW(), 
#                 utc_offset TEXT  
#             )
#         """)
#     except:

    
        
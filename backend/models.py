import os
import psycopg2
import logging

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    conn = None
    cur = None
    try:
        # Fetch database connection details
        dbname = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = int(os.getenv("DB_PORT"))

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()

        # Create table query
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_registration
        (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_table_query)
        conn.commit()

        logger.info("Database connected and table created successfully.")

    except Exception as e:
        logger.error(f"Failed to create database table: {str(e)}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

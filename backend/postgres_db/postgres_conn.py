import os
import psycopg2
import datetime
import logging
from werkzeug.security import check_password_hash 
from flask import jsonify, request

from dotenv import load_dotenv
load_dotenv()

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Helper function to connect to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT"))
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def user_registration_insert_db(username, email, password_hash):
    created_at=datetime.datetime.now()

    try:
        # Step 1: Check if the email already exists
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id FROM user_registration WHERE email = %s", (email, )
                )
                existing_user = cur.fetchone()

                # If the email already exists, raise an error
                if existing_user:
                    return jsonify({"message": "Email already exists. Please use a different email address.","email":email}), 400

        # Step 2: If email does not exist, proceed with registration

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Insert user registration data
                cur.execute(
                    "INSERT INTO user_registration (username, email, password_hash, created_at) "
                    "VALUES (%s, %s, %s, %s) RETURNING user_id",
                    (username, email, password_hash, created_at)
                )
                user_id = cur.fetchone()[0]
                conn.commit()

    except Exception as e:
        logger.error(f"Error during user registration insert: {str(e)}")
        raise

# User login check
def user_login_db(email, password):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Step 1: Check if email exists
                cur.execute(
                    "SELECT user_id, username, password_hash FROM user_registration WHERE email = %s", (email,)
                )
                user = cur.fetchone()

                if not user:
                    return jsonify({"error":"Invalid email or password. Please enter valid credentials."}), 400

                user_id, username, stored_hash = user

                # Check validate password
                if check_password_hash(stored_hash, password):
                    # Password is correct
                    logger.info(f"User '{username}' (ID '{user_id}) logged in successfully ")
                    return jsonify({"message":"Login successfully!", "user_id":user_id, "username":username}), 200
                else:
                    logger.error(f"Login failed: Incorrect password for email '{email}'.")
                    return jsonify({"error":"Invalid email or password."}), 401

    except Exception as e:
        logger.error(f"Error during user login: {str(e)}")
        return jsonify({"error":"Internal server error"}), 500

import os
import datetime
import smtplib

from flask import jsonify

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from werkzeug.security import check_password_hash 

from postgres_db.postgres_conn import user_registration_insert_db, user_login_db

from dotenv import load_dotenv
load_dotenv()

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load env variables
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Function to send email via SMTP
def send_email(user_email):
    try:
        # Email content
        subject = "Welcome to Trade Ticker"
        message = f"""
        Hello {user_email}, 

        Welcome to Trade Ticker
        
        We're excited to have you on board. with our platform, you can easily monitor live stock prices, get instant alerts, adn stay ahead in the market
        
        Start exploring and make the most of your investing journey.
        
        Happy Tracking!
        - Team Trade Ticker"""

        # Setup the MIME message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message,'plain'))

        # Connect to the SMTP server and send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls() # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            logger.info(f"Mail send to {user_email}")
    
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise

def user_registration_insert(username, email, password_hash):
    try:
        response = user_registration_insert_db(username, email, password_hash)
        return response
    except Exception as e:
        logger.error(f"Error in user_registration_insert: {str(e)}")
        return jsonify({"error": "Internal server error during registration"}), 500


def user_login(email,password):
     return user_login_db(email,password) 



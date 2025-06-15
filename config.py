import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # Other configurations
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("DEBUG") == "True"

    # Load SECRET_KEY from environment variables
    SECRET_KEY = os.getenv("SECRET_KEY")  # Ensure SECRET_KEY is loaded from .env file

      # Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

# import secrets

#  Generate a random 24-character secret key (it’s a good idea to have a key of sufficient length)
# secret_key = secrets.token_hex(16)  # This gives a 32-character hex string

# print(secret_key)

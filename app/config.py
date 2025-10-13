import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key")  # Add a secret for JWT
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_SORT_KEYS = False

    DB_SCHEMA = os.environ.get("DB_SCHEMA")  # e.g. "public"

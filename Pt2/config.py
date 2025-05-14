import os

class Config:
    SECRET_KEY = 'your_secret_key'  # Replace with a secure value
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "study-tracker-secret-key")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///study_tracker.db"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

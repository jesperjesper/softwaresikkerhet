import os
from datetime import timedelta

class Config:
    SECRET_KEY = '123swag'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Login settings
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    #limiter
    RATELIMIT_STORAGE_URL = "memory://"

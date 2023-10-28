import os
from datetime import timedelta

class Settings:
    # Configuración general
    APP_NAME = 'MiniBlog'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = True

    # Configuración SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuracion JWT Token
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Configuracion Redis
    REDIS_URL = os.environ.get('REDIS_URL')

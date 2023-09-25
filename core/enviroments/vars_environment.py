import os

from .base_config import BaseConfig

class Configuration(BaseConfig):
    DEBUG = os.getenv('DEBUG')
    ENV_NAME = os.getenv('ENV_NAME')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    LOGIN_EXPIRE_TIME = os.getenv('LOGIN_EXPIRE_TIME')
    CRYPTO_SECRET_KEY = f"{os.getenv('CRYPTO_SECRET_KEY')}".encode()
    DEFAULT_PASSWROD = os.getenv('DEFAULT_PASSWROD',None) or "sqlite:///data.db"
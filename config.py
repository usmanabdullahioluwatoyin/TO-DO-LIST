import os
from dotenv import  load_dotenv

class Config:
    db_user = os.getenv("DATABASE_USER")
    db_password = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOST")
    db_name = os.getenv("DATABASE_NAME")
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"


class Development(Config):
    DEBUG = True

class Production(Config):
    DEBUG = False

config = {
    "development": Development,
    "production" : Production
}

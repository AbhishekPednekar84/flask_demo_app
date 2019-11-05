import dotenv
import os

dotenv.load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    DEBUG = False
    LOGIN_DISABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DevConfig(Config):
    DEBUG = True

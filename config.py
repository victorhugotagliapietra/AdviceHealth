import os

class Config:
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:123@localhost:5432/postgres')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback_jwt_secret_key')

class TestingConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_TEST_URL', 'postgresql://postgres:123@localhost:5432/test_database')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'fallback_jwt_secret_key_for_testing')
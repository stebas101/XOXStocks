import pytest

from app import create_app, db
from app.models import User

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # using a memory only database

def test_password_hashing():
    u = User(username='stefano', email='stefano@exampletesting.info')
    pass
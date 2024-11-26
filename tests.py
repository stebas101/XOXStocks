import os
os.environ['DATABASE_URL'] = 'sqlite://' # TODO is this necessary?

from datetime import datetime, timezone, timedelta
import unittest

from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # using a memory only database


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_hashing(self):
        u = User(username='stefano', email='stefano@exampletesting.info')
        u.set_password('youllneverguessme')
        self.assertFalse(u.check_password('foobar'))
        self.assertTrue(u.check_password('youllneverguessme'))
    
    def test_user(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add_all([u1, u2])
        
        db.session.commit()
        pass

          
if __name__ == '__main__':
    unittest.main(verbosity=2)
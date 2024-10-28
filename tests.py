import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest

from flask import current_app
from app import db
# from app.models import User, Post

data_path = os.path.join(current_app.instance_path, 'data/')

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    print('hello')
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
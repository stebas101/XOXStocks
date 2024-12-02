import pytest
import os

from app import create_app, db
from app.models import User, Watchlist, Symbol
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # using a memory only database
    SYMBOL_DATA_PATH = os.environ.get('SYMBOL_DATA_PATH') or 'data'
    
    
@pytest.fixture
def flask_context():
    #setup
    app = create_app(TestConfig)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    
    yield
    
    #teardown
    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_password_hashing():
    u = User(username='stefano', email='stefano@exampletesting.info')
    u.set_password('youllneverguessme')
    assert u.check_password('foobar') == False
    assert u.check_password('youllneverguessme') == True
    
def test_user(flask_context):
    u1 = User(username='john', email='john@example.com')
    u2 = User(username='susan', email='susan@example.com')
    db.session.add_all([u1, u2])
    db.session.commit()

def test_watchlists(flask_context):
    list1 = Watchlist(list_name='My List', symbol_list='AAPL,NVDA,TSLA', user_id='5')
    db.session.add(list1)
    db.session.commit()

def test_load_symbols(flask_context):
    pass

def test_update_symbols(flask_context):
    pass


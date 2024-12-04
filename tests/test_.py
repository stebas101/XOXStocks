import pytest
import os

import sqlalchemy as sa

from app import create_app, db
from app.models import User, Watchlist
from config import Config
# from app.routes import add_watchlist
from findata import get_stock_info


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
    

def mock_list():
    LIST='AAPL,NVDA,TSLA'
    LIST_NAME = 'My List'
    symbol_list = LIST.split(',')
    watchlist = Watchlist(user=1, list_name=LIST_NAME)
    for symbol in symbol_list:
        watchlist.add_symbol(symbol)
    return watchlist


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

def test_add_symbols_to_wl(flask_context):
    watchlist = mock_list()
    assert watchlist.get_watchlist()


def test_add_existing_symbol_to_wl(flask_context):
    watchlist = mock_list()
    symbol = watchlist.get_watchlist()[0]
    assert watchlist.add_symbol(symbol) == False


def test_remove_symbol_from_wl(flask_context):
    watchlist = mock_list()
    to_remove = watchlist.get_watchlist()[-1]
    watchlist.remove_symbol(to_remove)
    assert to_remove not in watchlist.get_watchlist()


def test_load_symbols(flask_context):
    pass

def test_update_symbols(flask_context):
    pass

def test_get_stock_info():
    get_stock_info('MSFT')


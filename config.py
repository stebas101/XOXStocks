"""
This module loads the environement variables from .env and provides a Config class
that passes those environment variables.
"""

import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """
    This class contains the environment variables as class vaiables.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(current_app.instance_path, 'database.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join('database.db')
    # sqlite:///path/to/database.db
    # postgresql://username:password@host:port/database_name
    # mysql://username:password@host:port/database_name
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SYMBOL_DATA_PATH = os.environ.get('SYMBOL_DATA_PATH') or 'data'
    
    POSTS_PER_PAGE = 20

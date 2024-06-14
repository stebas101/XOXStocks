from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String[64], unique=True, nullable=False)
    password = db.Column(db.String[256], nullable=False)
    # email = db.Column(db.String(80), unique=True, nullable=False)
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Symbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String[32], unique=True, nullable=False, index=True)
    venue = db.Column(db.String[32], nullable=True)
    short_name = db.Column(db.String[128])
    
    def __repr__(self):
        return f'<Symbol {self.symbol}@{self.venue}: {self.short_name}>'
    
class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) # TODO foreign key
    symbol_list = db.Column(db.Text)

    def __repr__(self):
        return f'<Watchlist {self.name}: user {self.user_id}>'
    
class DefaultList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String[128], nullable=False)
    symbol_list = db.Column(db.Text)
    
    def __repr__(self):
        return f'<DefaultList {self.name}>'
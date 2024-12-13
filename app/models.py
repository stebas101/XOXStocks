from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    
    # watchlists: so.WriteOnlyMapped['Watchlist'] = so.relationship(
    #     back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_reset_password_token(self, expires_in=600):
        pass
    
    @staticmethod
    def verify_reset_password_token(token):
        pass
    
    def set_watchlist(self):
        pass


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Symbol(db.Model):
    __tablename__ = 'symbols'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    symbol: so.Mapped[str] = so.mapped_column(sa.String(16),
                                            index=True,
                                            unique=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    
    def __repr__(self):
        return f'<Symbol {self.symbol}: {self.name}>'
    
    def update(self, symb_new):
        self.name = symb_new.name


class Watchlist(db.Model):
    __tablename__ = 'watchlists'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    list_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    symbol_list: so.Mapped[str] = so.mapped_column(sa.Text())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    
    def __init__(self, user: int, list_name: str):
        self.user_id = user
        self.list_name = list_name
        self.symbol_list = ''
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Watchlist {self.list_name}: user {self.user_id}>'
    
    def add_symbol(self, symbol: str) -> bool:
        current_list = self.symbol_list.split(',')
        if symbol not in current_list:
            add = ',' + symbol.upper() if self.symbol_list != '' else symbol.upper()
            self.symbol_list += add
            db.session.commit()
            return True
        return False
    
    def remove_symbol(self, symbol: str) -> bool:
        symbol_list = self.symbol_list.split(',')
        if symbol in symbol_list:
            del symbol_list[symbol_list.index(symbol)]
            self.symbol_list = ','.join(symbol_list)
            db.session.commit()
            return True
        return False
    
    def get_watchlist(self) -> list[str]:
        return self.symbol_list.split(',')
    
    def rename(self, new_name: str) -> None:
        self.list_name = new_name
        db.session.commit()
    

# class DefaultList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String[128], nullable=False)
#     symbol_list = db.Column(db.Text, nullable=False)
    
#     def __repr__(self):
#         return f'<DefaultList {self.name}>'
from datetime import datetime, timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))

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


# class Symbol(db.Model):
#     id: so.Mapped[int] = so.mapped_column(primary_key=True)
#     symbol: so.Mapped[str] = so.mapped_column(sa.String(32), index=True,
#                                                 unique=True)
#     venue: so.Mapped[str] = so.mapped_column(sa.String(32))
#     short_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    
#     def __repr__(self):
#         return f'<Symbol {self.symbol}@{self.venue}: {self.short_name}>'


# class Watchlist(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False) # TODO foreign key
#     name = db.Column(db.Text, nullable=False)
#     symbol_list = db.Column(db.Text, nullable=False)

#     def __repr__(self):
#         return f'<Watchlist {self.name}: user {self.user_id}>'


# class DefaultList(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String[128], nullable=False)
#     symbol_list = db.Column(db.Text, nullable=False)
    
#     def __repr__(self):
#         return f'<DefaultList {self.name}>'
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so

from . import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    # email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
    #                                          unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # created_at = db.Column(db.DateTime(timezone=True),
    #                     server_default=func.now())
    
    def __repr__(self):
        return f'<User {self.username}>'
    
# in flask shell:
# from app import db, User
# db.drop_all()
# db.create_all()

# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
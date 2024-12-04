from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
import sqlalchemy as sa

from app import db
from app.models import User, Watchlist


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                        DataRequired(),
                        Length(min=6, max=16, message='Username must be between 6 and 16 characters long.')
                        ])
    email = StringField('Email', validators=[
                        DataRequired(),
                        Email()
                        ])
    password = PasswordField('Password', validators=[
                        DataRequired()
                        ])
    repeat = PasswordField('Repeat Password', validators=[
                        DataRequired(),
                        EqualTo('repeat', message='Passwords must match.')
                        ])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Username already in use.')
    
    def validate_email(self, email: object) -> None:
        email = db.session.scalar(
            sa.select(User).where(
                User.email == email.data))
        if email is not None:
            raise ValidationError('Email already in use.')


class ResetPasswordRequestForm(FlaskForm):
    pass


class ResetPasswordForm(FlaskForm):
    pass

class AddListForm(FlaskForm):
    list_name = StringField('Watchlist Name', validators=[DataRequired(),
                                                          Length(min=4, message="List Name must be at least 4 characters long")])
    submit = SubmitField('Add Watchlist')
    
    def validate_list_name(self, list_name: object) -> None:
        watchlist = db.session.scalar(
            sa.select(Watchlist).where(
                Watchlist.list_name == list_name.data).where(Watchlist.user_id == current_user.id))
        if watchlist is not None:
            raise ValidationError('List name already in use.')
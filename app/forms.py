from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
import sqlalchemy as sa

from app import db
from app.models import User


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
    
    def validate_email(self, email):
        pass


class ResetPasswordRequestForm(FlaskForm):
    pass


class ResetPasswordForm(FlaskForm):
    pass
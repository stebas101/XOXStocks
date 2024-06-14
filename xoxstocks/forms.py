from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                        DataRequired(),
                        Length(min=6, max=12, message='Username must be between 6 and 12 characters long.')
                        ])
    password = PasswordField('Password', validators=[
                        DataRequired(),
                        EqualTo('repeat', message='Passwords must match.')])
    repeat = PasswordField('Repeat Password', validators=[DataRequired()])
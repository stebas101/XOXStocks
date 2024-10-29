import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash

# from xoxstocks.db import get_db

from app import db
from app.forms import RegisterForm, LoginForm
from app.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():        
        user = User(username = form.data['username'],
                    password = generate_password_hash(form.data['password']))
        error = None

        try:
            db.session.add(user)
            db.session.commit()
            flash('Thank you for registering!')
        except:
            error = f"User {user.username} is already registered."
        else:
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user) # TODO add remember_me option
        # next_page = request.args.get('next')
        # if not next_page or urlsplit(next_page).netloc != '':
        #     next_page = url_for('main.index')
        # return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user =  User.query.filter(User.id == user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    flash("You're now logged out.")
    return redirect(url_for('index'))


# require authentication in other views
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
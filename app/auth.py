import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa

from app import db
from app.forms import RegisterForm, LoginForm
from app.models import User, Watchlist


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # adding user
        username_in = form.data['username']
        password_in = form.data['password']
        email_in = form.data['email']
        # TODO check email is not in use
        user = User(username = username_in,
                    email = email_in)
        user.set_password(password_in)
        db.session.add(user)
        db.session.commit()
        
        # adding default watchlist
        user_data = db.session.scalar(
            sa.select(User).where(User.username == username_in)
        )
        Watchlist(user = user_data.id,
                  list_name=current_app.config['DEFAULT_WATCHLIST_NAME']
                  )

        flash('Thank you for registering!')
        
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',
                           title='Register',
                           form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.data['username']
        password = form.data['password']
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user) # TODO add remember_me option
        # TODO remember next page after login
        # next_page = request.args.get('next')
        # if not next_page or urlsplit(next_page).netloc != '':
        #     next_page = url_for('main.index')
        # return redirect(next_page)
        flash('Welcome into XOXStocks!')
        return redirect(url_for('index'))
    
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    flash("You're now logged out.")
    return redirect(url_for('index'))
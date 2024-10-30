from datetime import datetime, timezone

from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app import db


bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/watchlist')
@login_required
def watchlist():
    return render_template('watchlist.html')

@bp.route('/screener')
@login_required
def screener():
    return render_template('screener.html')

# this updates the last_seen field for each user
@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
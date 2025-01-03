from datetime import datetime, timezone

from flask import Blueprint, render_template, session
from flask_login import current_user, login_required

from app import db
from findata import get_stock_info


bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/stock_info/<symbol>')
@login_required
def stock_info(symbol: str):
    """
    Retrieves some stock info from YFinance and returns it as JSON
    """
    return get_stock_info(symbol)


@bp.route('/screener')
@login_required
def screener():
    print(f"{session.get('watchlist_id') = }")
    return render_template('screener.html')


# this updates the last_seen field for each user
@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@bp.route('/user')
@login_required
def user():
    user = current_user
    return render_template('user.html', user=user)
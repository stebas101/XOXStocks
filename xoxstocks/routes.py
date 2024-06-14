from flask import (
    Blueprint, redirect, render_template,
    url_for
)

from xoxstocks.auth import login_required


bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('watchlist')
@login_required
def watchlist():
    return render_template('watchlist.html')


@bp.route('screener')
@login_required
def screener():
    return redirect(url_for('index'))

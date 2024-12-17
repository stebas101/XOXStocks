from flask import Blueprint, render_template, session
from flask_login import login_required


bp = Blueprint('screener', __name__, url_prefix='/screener')

@bp.route('/screener')  # TODO remame this and change in layout.html too
@login_required
def screener():
    watchlist_id = session.get('watchlist_id')
    return render_template('screener/screener.html')
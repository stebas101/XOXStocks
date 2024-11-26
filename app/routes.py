from datetime import datetime, timezone

from flask import Blueprint, render_template, request, g
from flask_login import current_user, login_required
import sqlalchemy as sa

from app import db
from app.models import Symbol, Watchlist, User


bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/watchlist')
@login_required
def watchlist():
    list_type = request.args.get('list')
    watchlist_id = request.args.get('wl_id')
    watchlist_id = int(watchlist_id) if watchlist_id else watchlist_id
    # TODO push watchlist_id to g
    # TODO if watchlist id = None, select a watchlist by default
    
    if list_type == 'wl':
        watchlists = db.session.scalars(
            sa.select(Watchlist).where(Watchlist.user_id == current_user.id)
        )
        watchlist_ids = [ {'id':watchlist.id, 'list_name':watchlist.list_name} for watchlist in list(watchlists) ]
    
    if list_type == 'wl' and not watchlist_id:        
        
        return render_template('watchlist.html',
                               list_type=list_type,
                               watchlist_ids=watchlist_ids
                               )
        
    if list_type == 'wl' and watchlist_id:
        # TODO push watchlist_id to g
        list_data = {}
       
        watchlist = db.session.scalar(
            sa.select(Watchlist).where(Watchlist.id == watchlist_id)
        )
        list_data['list_name'] = watchlist.list_name
        list_data['id'] = watchlist_id
        list_data['list'] = []
        symbols = watchlist.symbol_list.split(',')
        for symbol in symbols:
            symbol_data = db.session.scalar(
                sa.select(Symbol).where(Symbol.symbol == symbol.upper())
            )
            list_data['list'].append({'symbol' : symbol_data.symbol,
                                'name' : symbol_data.name,
                                })
        
        return render_template('watchlist.html',
                               list_type=list_type,
                               watchlist_id=watchlist_id, # TODO redundant: remove and use list_data['id']
                               watchlist_ids=watchlist_ids,
                               list_data=list_data,
                            )
        
    return render_template('watchlist.html',
                           list_type=list_type,
                        #    watchlist_id=watchlist_id,
                        #    list_data=list_data,
                           )

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

@bp.route('/user')
@login_required
def user():
    user = current_user
    return render_template('user.html', user=user)
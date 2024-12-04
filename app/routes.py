from datetime import datetime, timezone

from flask import Blueprint, render_template, request, g, current_app, url_for, flash, redirect
from flask_login import current_user, login_required
import sqlalchemy as sa

from app import db
from app.models import Symbol, Watchlist
from app.forms import AddListForm
from findata import get_stock_info


bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/watchlist')
@login_required
def watchlist():
    list_type = request.args.get('list')
    watchlist_id = request.args.get('wl_id', type=int)
    page = request.args.get('page', 1, type=int)
    form = AddListForm()
    # TODO push watchlist_id to g
    # TODO if watchlist_id = None, select a watchlist by default
    
    if list_type == 'wl':
        watchlists = db.session.scalars(
            sa.select(Watchlist).where(Watchlist.user_id == current_user.id)
        )
        watchlist_ids = [ {'id':watchlist.id, 'list_name':watchlist.list_name} for watchlist in list(watchlists) ]
    
    if list_type == 'wl' and not watchlist_id:        
        
        return render_template('watchlist.html',
                               list_type=list_type,
                               watchlist_ids=watchlist_ids,
                               form=form,
                               )
        
    if list_type == 'wl' and watchlist_id:
        # TODO push watchlist_id to g
        # TODO check for empty watchlist
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
                               watchlist_id=watchlist_id,
                               watchlist_ids=watchlist_ids,
                               list_data=list_data,
                               form=form,
                               )
        
    if list_type =='all':
        symbol_data = {}
        query = sa.select(Symbol).order_by(Symbol.name.asc())
        symbols = db.paginate(query,
                              page=page,
                              per_page=current_app.config['POSTS_PER_PAGE'],
                              error_out=False
                              )
        pages = symbols.pages
        next_url = url_for('/.watchlist', page=symbols.next_num) if symbols.has_next else None
        prev_url = url_for('/.watchlist', page=symbols.prev_num) if symbols.has_prev else None
        
        for symbol in symbols.items:
            info: dict = get_stock_info(symbol.symbol)
            symbol_data[symbol.symbol] = info
        
        return render_template('watchlist.html',
                               list_type=list_type,
                               watchlist_id=watchlist_id,
                               symbol_data=symbol_data,
                            #    symbols=symbols.items,
                               pages=pages,
                               page=page,
                               next_url=next_url,
                               prev_url=prev_url,
                               )
        
    return render_template('watchlist.html',
                           list_type=list_type,
                           form=form,
                           )
    
@bp.route('/add_watchlist', methods=('GET', 'POST'))
@login_required
def add_watchlist():
    form = AddListForm()
    list_name = form.data['list_name']
    if form.validate_on_submit():
        Watchlist(current_user.id, list_name)
        flash(f"Watchlist {list_name} added.")
    else:
        flash(f"Watchlist {list_name} could not be added.")
    return redirect(url_for("/.watchlist")+"?list=wl") 
 

def del_watchlist(list_id: int) -> None:
    pass


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
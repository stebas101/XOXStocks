from datetime import datetime, timezone

from flask import Blueprint, render_template, request, current_app, url_for, flash, redirect, session
from flask_login import current_user, login_required
import sqlalchemy as sa

from app import db
from app.models import Symbol, Watchlist, User
from app.forms import AddListForm
from findata import get_stock_info


bp = Blueprint('/', __name__, url_prefix='/')

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('watchlist')
@login_required
def watchlist():
    """
    This is the route that is used the first time a user accesses the 'My Watchlist' feature.
    The function checks if there is a valid watchlist_id that can be used. If so, it resirects
    to /watchlist/wl. Otherwise, it renders a page without watchlist table and flashes a message
    asking to create a new watchlist.
    """
    form = AddListForm() # the form is used in 'Select Watchlist'
    list_type = 'wl'
    watchlist_id = session.get('watchlist_id')
    
    # check if current watchlist_id is valid for the current user
    query = sa.select(Watchlist).where(Watchlist.user_id == current_user.id)
    user_watchlists = db.session.scalars(query).all()
    if watchlist_id in [wl.id for wl in user_watchlists]: # watchlist_id is valid
        print(url_for("/.watchlist"))
        return redirect(url_for('/.watchlist') + "/wl")
    else:
        watchlist_id = get_default_watchlist(current_user.id)
        if watchlist_id: # if there's a watchlist to use
            session.watchlist_id = watchlist_id
            return redirect(url_for('/.watchlist') + "/wl")

    flash("You have no watchlist to use. Create a new one.")
    return render_template('watchlist.html',
                           list_type=list_type,
                           form=form,
                           )


@bp.route('/watchlist/wl')
@login_required
def watchlist_id():
    # TODO: check there's a valid watchlist, or render an error
    list_type = 'wl'
    form = AddListForm()
    # use requested watchlist or watchlist in session if that exists
    watchlist_id = session.get('watchlist_id')
    watchlist_id = request.args.get('wl_id', watchlist_id, type=int)
    # if the watchlist does not belong to the user or does not exist, redirect to default watchlist page:
    if watchlist_id not in get_user_watchlists(current_user.id):
        return redirect('/watchlist')
    # set session watchlist to the requested one:
    session.watchlist_id = watchlist_id
    page = request.args.get('page', 1, type=int)
    # preparing watchlist data to display as available options
    watchlists = db.session.scalars(
        sa.select(Watchlist).where(Watchlist.user_id == current_user.id)
    )
    watchlist_ids = [ {'id':watchlist.id, 'list_name':watchlist.list_name} for watchlist in list(watchlists) ]
    
    # preparing data to display as watchlist
    list_data = {}
    watchlist = db.session.scalar(
        sa.select(Watchlist).where(Watchlist.id == watchlist_id)
    )
    list_data['list_name'] = watchlist.list_name
    list_data['id'] = watchlist_id
    list_data['list'] = []
    
    if len(watchlist.symbol_list) == 0:
        list_data = None
    else:    
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


@bp.route('/watchlist/indices')
@login_required
def indices():
    return "On Indices"

@bp.route('/watchlist/all')
@login_required
def all_symbols():
    list_type = 'all'
    form = AddListForm() # the form is used in 'Select Watchlist'
    page = request.args.get('page', 1, type=int)
    # TODO check watchlist belongs to the user
    watchlist_id = session.get('watchlist_id')
    # TODO get watchlist ids for the menu
    symbol_data = {}
    query = sa.select(Symbol).order_by(Symbol.name.asc())
    symbols = db.paginate(query,
                        page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False
                        )
    pages = symbols.pages
    # TODO fix url_for
    next_url = url_for('/.watchlist', page=symbols.next_num) if symbols.has_next else None
    prev_url = url_for('/.watchlist', page=symbols.prev_num) if symbols.has_prev else None
    
    for symbol in symbols.items:
        info: dict = get_stock_info(symbol.symbol)
        symbol_data[symbol.symbol] = info
        
    return render_template('watchlist.html',
                            list_type=list_type,
                            watchlist_id=watchlist_id,
                            symbol_data=symbol_data,
                            form=form,
                        #    symbols=symbols.items,
                            pages=pages,
                            page=page,
                            next_url=next_url,
                            prev_url=prev_url,
                            )
    

def get_default_watchlist(user_id: int) -> int:
    """This function returns a valid watchlist_id for a user.

    Returns:
        int: watchlist_id or 0 if no valid watchlist can be found
    """
    query = sa.select(Watchlist).where(Watchlist.user_id == user_id).order_by(Watchlist.id.asc())
    watchlist = db.session.scalars(query).first()
    return watchlist.id if watchlist else 0

def get_user_watchlists(user_id: int) -> list[int]:
    """This returns a list of the watchlist ids belonging to a user.

    Args:
        user_id (int): user id

    Returns:
        list[int]: list of watchlist ids
    """
    query = sa.select(Watchlist).where(Watchlist.user_id == current_user.id)
    user_watchlists = db.session.scalars(query).all()
    return [wl.id for wl in user_watchlists]


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
from flask import (Blueprint, current_app, session, flash, redirect, url_for,
                   render_template, redirect, request)
from flask_login import current_user, login_required
import sqlalchemy as sa

from app import db
from app.models import Watchlist, Symbol
from app.forms import AddListForm
from findata import get_stock_info


bp = Blueprint('watchlist', __name__, url_prefix='/wl')

@bp.route('/default')
@login_required
def default():
    """
    This is the route that is used the first time a user accesses the 'My Watchlist' feature.
    The function checks if there is a valid watchlist_id that can be used. If so, it resirects
    to /watchlist/wl. Otherwise, it renders a page without watchlist table and flashes a message
    asking to create a new watchlist.
    """
    list_type = 'wl' # used to determine the active navigation link
    form = AddListForm() # the form is used in 'Select Watchlist'
    watchlist_id = session.get('watchlist_id')
    watchlist_ids = get_user_watchlist_data(current_user.id)
    user_watchlists = [wl['id'] for wl in watchlist_ids] # ids of watchlists belonging to user
    
    # TODO refactor this:
    # check if current watchlist_id is valid for the current user
    if watchlist_id and watchlist_id in user_watchlists: # watchlist_id is valid
        return redirect(url_for('watchlist.watchlist'))
    else:
        watchlist_id = get_default_watchlist(current_user.id)
        session['watchlist_id'] = watchlist_id
        if watchlist_id: # if there's a watchlist to use
            session['watchlist_id'] = watchlist_id
            return redirect(url_for('watchlist.watchlist'))

    flash("You have no watchlist to use. Create a new one.")
    return render_template('watchlist/watchlist.html',
                           list_type=list_type,
                           form=form,
                           watchlist_id=watchlist_id,
                           watchlist_ids=watchlist_ids,
                           )


@bp.route('/watchlist')
@login_required
def watchlist():
    list_type = 'wl'
    page = request.args.get('page', 1, type=int)
    form = AddListForm() # the form is used in 'Select Watchlist'
    watchlist_id = session.get('watchlist_id')
    watchlist_ids = get_user_watchlist_data(current_user.id)
    user_watchlists = [wl['id'] for wl in watchlist_ids] # ids of watchlists belonging to user

    # if the watchlist does not belong to the user or does not exist, redirect to default watchlist page:
    if watchlist_id not in user_watchlists:
        session['watchlist_id'] = get_default_watchlist(current_user.id)
        return redirect(url_for('watchlist.default'))

    # preparing stock data to display for a watchlist
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
    
    return render_template('watchlist/watchlist.html',
                            list_type=list_type,
                            watchlist_id=watchlist_id,
                            watchlist_ids=watchlist_ids,
                            list_data=list_data,
                            form=form,
                            )


@bp.route('/indices')
@login_required
def indices():
    return "On Indices"


@bp.route('/all')
@login_required
def all_symbols():
    #
    # TODO case with no active list
    #
    list_type = 'all'
    page = request.args.get('page', 1, type=int)
    form = AddListForm() # the form is used in 'Select Watchlist'
    watchlist_id = session.get('watchlist_id')
    watchlist_ids = get_user_watchlist_data(current_user.id)
    user_watchlists = [wl['id'] for wl in watchlist_ids] # ids of watchlists belonging to user
    active_watchlist = db.session.scalar(
        sa.select(Watchlist).where(Watchlist.id == watchlist_id)
    )

    # if the watchlist does not belong to the user or does not exist, redirect to default watchlist page:
    if watchlist_id not in user_watchlists:
        session['watchlist_id'] = get_default_watchlist(current_user.id)
        
    active_watchlist = db.session.scalar(
        sa.select(Watchlist).where(Watchlist.id == watchlist_id)
    )
    watchlist_symbols = active_watchlist.symbol_list.split(',')

    symbol_data = {}
    query = sa.select(Symbol).order_by(Symbol.name.asc())
    symbols = db.paginate(query,
                        page=page,
                        per_page=current_app.config['POSTS_PER_PAGE'],
                        error_out=False
                        )
    pages = symbols.pages
    next_url = url_for('watchlist.all_symbols', page=symbols.next_num) if symbols.has_next else None
    prev_url = url_for('watchlist.all_symbols', page=symbols.prev_num) if symbols.has_prev else None
    
    for symbol in symbols.items:
        info: dict = get_stock_info(symbol.symbol)
        symbol_data[symbol.symbol] = info
        
    return render_template('watchlist/watchlist.html',
                            list_type=list_type,
                            watchlist_id=watchlist_id,
                            watchlist_ids=watchlist_ids,
                            watchlist_symbols=watchlist_symbols,
                            symbol_data=symbol_data,
                            form=form,
                            pages=pages,
                            page=page,
                            next_url=next_url,
                            prev_url=prev_url,
                            )


@bp.route('/select_watchlist/<wl>')
@login_required
def select_watchlist(wl: str):
    session['watchlist_id'] = int(wl)
    print(f"{session.get('watchlist_id') = }")

    return redirect(request.referrer)


@bp.route('/add_watchlist', methods=('POST',))
@login_required
def add_watchlist():
    form = AddListForm()
    list_name = form.data['list_name']
    if form.validate_on_submit():
        Watchlist(current_user.id, list_name)
        flash(f"Watchlist {list_name} added.")
    else:
        flash(f"Watchlist {list_name} could not be added.")
    return redirect(url_for("watchlist.default"))


@bp.route('/rename_watchlist', methods=('POST',))
@login_required
def rename_watchlist():
    form = AddListForm()
    watchlist_id = session.get('watchlist_id')
    watchlist = db.session.scalar(
        sa.select(Watchlist).where(Watchlist.id == watchlist_id)
    )
    new_name = form.data['list_name']
    old_name = watchlist.list_name
    if form.validate_on_submit():
        watchlist.rename(new_name=new_name)
        flash(f"Watchlist {old_name} renamed as {new_name}.")
    else:
        flash(f"Watchlist {old_name} could not be renamed.")
    return redirect(url_for("watchlist.default")) 


@bp.route('/delete_watchlist', methods=('POST',))
@login_required
def delete_watchlist() -> None:
    watchlist_id = session.get('watchlist_id')
    watchlist = db.session.scalar(sa.select(Watchlist).where(Watchlist.id == watchlist_id))
    name = watchlist.list_name
    try:
        db.session.delete(watchlist)
        db.session.commit()
        flash(f"Watchlist {name} deleted.")
    except:
        flash(f"Watchlist {name} could not be deleted.")
    return redirect(request.referrer)


@bp.route('/add_to_watchlist', methods=['POST'])
@login_required
def add_to_watchlist():
    watchlist_id = session.get('watchlist_id')
    watchlist = db.session.scalar(sa.select(Watchlist).where(Watchlist.id == watchlist_id))
    symbol = request.form.get('symbol')
    added = watchlist.add_symbol(symbol)
    if added:
        flash(f"{symbol} was added to the active watchlist.")
    else:
        flash(f"{symbol} was already in the watchlist.")
    return redirect(request.referrer)


@bp.route('/remove_from_watchlist', methods=['POST'])
@login_required
def remove_from_watchlist():
    watchlist_id = session.get('watchlist_id')
    watchlist = db.session.scalar(sa.select(Watchlist).where(Watchlist.id == watchlist_id))
    symbol = request.form.get('symbol')
    print(watchlist_id, symbol)
    removed = watchlist.remove_symbol(symbol)
    if removed:
        flash(f"{symbol} was removed from the active watchlist.")
    else:
        flash(f"{symbol} could not be removed.")
    return redirect(request.referrer)


def get_default_watchlist(user_id: int) -> int:
    """This function returns a valid watchlist_id for a user.

    Returns:
        int: watchlist_id or 0 if no valid watchlist can be found
    """
    query = sa.select(Watchlist).where(Watchlist.user_id == user_id).order_by(Watchlist.id.asc())
    watchlist = db.session.scalars(query).first()
    return watchlist.id if watchlist else 0

def get_user_watchlist_data(user_id: int) -> list[dict]:
    """This function returns a list that includes data (id and list_name) for each watchlist belonging
    to a user.

    Args:
        user_id (int): user id

    Returns:
        list[dict]: list of dicts containing data fot the watchlists.
    """

    # preparing watchlist data to display as available options
    watchlists = db.session.scalars(
        sa.select(Watchlist).where(Watchlist.user_id == user_id)
    )
    watchlist_ids = [ {'id':watchlist.id, 'list_name':watchlist.list_name} for watchlist in list(watchlists) ]
    return watchlist_ids

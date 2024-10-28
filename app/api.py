from flask import Blueprint, g, request, jsonify

from app import db
from app.models import Symbol


bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/symbols')
def symbols():
    table = []
    try:
        symbols = Symbol.query.all()
        for s in symbols:
            table.append((s.symbol, s.short_name))
        print(table)
        return jsonify(table)
    except:
        return 'database error' # TODO return proper error page

from flask import Blueprint, g, request, jsonify

from xoxstocks.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/symbols')
def symbols():
    db = get_db()
    try:
        result = db.execute(
                'SELECT * FROM asset;'
            ).fetchall()
        # for row in result:
        #     print(row['symbol'], row['short_name'])
        #     print(dict(result))
        return jsonify(dict(result))
    except:
        return 'error'


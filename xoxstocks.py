import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Symbol

app = create_app()


@app.shell_context_processor
def make_shell_context():
    # add classes to use in the flask shell:
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Symbol':Symbol} 
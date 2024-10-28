import os, click

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # TODO implement a config design
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    # sqlite:///path/to/database.db
    # postgresql://username:password@host:port/database_name
    # mysql://username:password@host:port/database_name
    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import routes
    app.register_blueprint(routes.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import api
    app.register_blueprint(api.bp)
    
    @app.cli.command("init-db")
    def init_db_command():
        """Clear the existing data and create new tables."""
        db.drop_all()
        db.create_all()
        click.echo('Initialized the database.')
        
    @app.cli.command("fill-data")
    def fill_data_command():
        from app.fill_data import fill_data
        fill_data()
        click.echo('Data filled into database.')
    
    return app

from app import models
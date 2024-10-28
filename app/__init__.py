import os

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app import routes
    app.register_blueprint(routes.bp)
    app.add_url_rule('/', endpoint='index')

    from app import auth
    app.register_blueprint(auth.bp)
    
    from app import api
    app.register_blueprint(api.bp)
    
    # @app.cli.command("init-db")
    # def init_db_command():
    #     """Clear the existing data and create new tables."""
    #     db.drop_all()
    #     db.create_all()
    #     click.echo('Initialized the database.')
        
    # @app.cli.command("fill-data")
    # def fill_data_command():
    #     from app.fill_data import fill_data
    #     fill_data()
    #     click.echo('Data filled into database.')
    
    return app

from app import models
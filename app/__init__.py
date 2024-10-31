import os

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # ensure the /instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app import routes
    app.register_blueprint(routes.bp)
    app.add_url_rule('/', endpoint='index')

    from app import auth
    app.register_blueprint(auth.bp)
    
    from app import cli
    app.register_blueprint(cli.bp)
    
    # from app import api
    # app.register_blueprint(api.bp)
    
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
    
    # TODO use this for email, logging and all activities not in dubugging or testing
    # if not app.debug and not app.testing:
        # if app.config['MAIL_SERVER']:
        #     auth = None
        #     if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        #         auth = (app.config['MAIL_USERNAME'],
        #                 app.config['MAIL_PASSWORD'])
        #     secure = None
        #     if app.config['MAIL_USE_TLS']:
        #         secure = ()
        #     mail_handler = SMTPHandler(
        #         mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        #         fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        #         toaddrs=app.config['ADMINS'], subject='Microblog Failure',
        #         credentials=auth, secure=secure)
        #     mail_handler.setLevel(logging.ERROR)
        #     app.logger.addHandler(mail_handler)

        # if not os.path.exists('logs'):
        #     os.mkdir('logs')
        # file_handler = RotatingFileHandler('logs/microblog.log',
        #                                    maxBytes=10240, backupCount=10)
        # file_handler.setFormatter(logging.Formatter(
        #     '%(asctime)s %(levelname)s: %(message)s '
        #     '[in %(pathname)s:%(lineno)d]'))
        # file_handler.setLevel(logging.INFO)
        # app.logger.addHandler(file_handler)

        # app.logger.setLevel(logging.INFO)
        # app.logger.info('Microblog startup')
    
    return app

from app import models
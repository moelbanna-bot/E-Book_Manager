from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

db = SQLAlchemy()
bootstrap = Bootstrap5()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(config.get(environment or 'development'))
    app.config["SECRET_KEY"] = "9e0f0d2b907e51edfaf9f1edfb436614"
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    from . import models
    migrate.init_app(app, db)
    register_apps(app)
    return app



def register_apps(application):
    from app.main.routes import main_blueprint
    from app.auth.routes import auth_blueprint
    application.register_blueprint(main_blueprint)
    application.register_blueprint(auth_blueprint, url_prefix='/auth')

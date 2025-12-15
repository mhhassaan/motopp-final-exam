from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from logging.config import dictConfig
from . import config
from typing import Any

# Configure database
db = SQLAlchemy()

# Configure logging
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def create_app() -> Flask:
    """
    Create a Flask application instance with database, authentication and logging configuration.

    :return: The created Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id: str) -> Any:
        """
        Load a user instance from the database.

        :param user_id: The ID of the user to load.
        :return: The loaded User instance, or None if not found.
        """
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .marketplace import market as market_blueprint
    app.register_blueprint(market_blueprint)

    with app.app_context():
        db.create_all()

    return app


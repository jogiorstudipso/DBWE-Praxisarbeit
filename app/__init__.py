"""App bootstrap.

Dieses File erstellt die Flask-Anwendung (Application Factory), initialisiert
globale Extensions und bindet alle Blueprints ein.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()
migrate = Migrate()

login = LoginManager()
# Nicht authentifizierte Nutzer werden zur Login-Route umgeleitet.
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'


def create_app(config_class=Config):
    # Application Factory: initialisiert App, Extensions und Blueprints.
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions werden hier an die konkrete App-Instanz gebunden.
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Fehlerseiten gelten app-weit (auch fuer API/HTML Responses).
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Auth-Routen leben unter /auth/*.
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Haupt-UI (Dashboard, Projekt- und Task-Seiten).
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # REST-API unter /api/*.
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


from app import models

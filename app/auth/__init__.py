"""Auth-Blueprint fuer Login/Logout/Registrierung."""

from flask import Blueprint

bp = Blueprint('auth', __name__)

# Import registriert die Routen beim Blueprint.
from app.auth import routes

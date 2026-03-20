"""API-Blueprint fuer token-geschuetzte JSON-Endpunkte."""

from flask import Blueprint

bp = Blueprint('api', __name__)

# Import registriert Auth-, Token-, Fehler- und Fachrouten.
from app.api import auth, tokens, errors, routes

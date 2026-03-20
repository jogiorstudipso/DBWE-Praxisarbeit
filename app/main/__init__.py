"""Main-Blueprint fuer die Web-Oberflaeche."""

from flask import Blueprint

bp = Blueprint('main', __name__)

# Import registriert die Routen beim Blueprint.
from app.main import routes

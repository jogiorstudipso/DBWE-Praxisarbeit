"""Errors-Blueprint mit globalen Fehlerhandlern."""

from flask import Blueprint

bp = Blueprint('errors', __name__)

# Import registriert Error-Handler beim Blueprint.
from app.errors import handlers

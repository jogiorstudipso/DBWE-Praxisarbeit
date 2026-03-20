"""Hilfsfunktionen fuer ein konsistentes API-Fehlerformat."""

from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException
from app.api import bp


def error_response(status_code, message=None):
    # Einheitliches Fehlerformat für alle API-Endpunkte.
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code


def bad_request(message):
    return error_response(400, message)


@bp.errorhandler(HTTPException)
def handle_exception(e):
    # Wandelt Werkzeug/Flask HTTP-Exceptions in JSON-Fehlerantworten um.
    return error_response(e.code)

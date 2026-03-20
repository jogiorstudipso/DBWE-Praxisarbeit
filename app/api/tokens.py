from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    # Erstellt (oder erneuert) ein zeitlich begrenztes Bearer-Token.
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return {'token': token}


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    # Invalidiert das aktuelle Token sofort durch abgelaufene Expiration.
    token_auth.current_user().revoke_token()
    db.session.commit()
    return '', 204

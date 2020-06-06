from datetime import datetime, timedelta
import jwt

from config.development import config


def encode(user):
    payload = {
        'user_id': user['user_id'],
        'exp': datetime.utcnow() + timedelta(seconds=config['JWT_EXP_DELTA_SECONDS'])
    }
    jwt_token = jwt.encode(
        payload, config['JWT_SECRET'], config['JWT_ALGORITHM'])

    return {'token': jwt_token.decode('utf-8')}


def decode(jwt_token):
    try:
        payload = jwt.decode(jwt_token, config['JWT_SECRET'], algorithms=[
                             config['JWT_ALGORITHM']])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return {'user_id': ''}

    return {'user_id': payload['user_id']}

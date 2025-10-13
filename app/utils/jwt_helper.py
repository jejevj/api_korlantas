import jwt
import datetime
from flask import current_app

def generate_token(user_id: int, username: str, role_id: int):
    """
    Generate a JWT token valid for 1 day.
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {
        "user_id": user_id,
        "username": username,
        "role_id": role_id,
        "exp": expiration_time
    }
    
    # Create the JWT token (sign it with the SECRET_KEY)
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")
    return token

def decode_token(token: str):
    """
    Decodes the JWT token and returns the payload.
    Returns None if the token is invalid or expired.
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        # Token is expired
        raise Exception("Token has expired.")
    except jwt.InvalidTokenError:
        # Token is invalid or the signature verification failed
        raise Exception("Invalid token.")
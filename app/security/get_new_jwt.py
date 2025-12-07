import datetime
import os

from jose import jwt

SECRET_KEY = os.environ.get("JWT_SECRET")


def get_new_jwt(openid):
    expiration = datetime.datetime.now(
        tz=datetime.timezone.utc) + datetime.timedelta(days=1)
    token = jwt.encode({
        "pld": openid.model_dump(),
        "exp": expiration,
        "sub": openid.id
    }, key=SECRET_KEY, algorithm="HS256")

    return {
        "token": token,
        "expiration": expiration
    }

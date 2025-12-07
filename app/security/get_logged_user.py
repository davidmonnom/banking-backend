import os

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyCookie
from jose import jwt
from sqlalchemy.orm import Session

from .. import schemas, utils
from .get_db import get_db

SECRET_KEY = os.environ.get("JWT_SECRET")

async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token")), db: Session = Depends(get_db)) -> schemas.User:
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""

    try:
        claims = jwt.decode(cookie, key=SECRET_KEY, algorithms=["HS256"])
        user = utils.user.get_by_external_id(db, external_id=claims["sub"])

        if not user:
            raise HTTPException(
                status_code=500, detail="Internal Server Error")

        return user
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials") from error

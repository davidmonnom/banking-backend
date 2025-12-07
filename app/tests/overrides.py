import os
import pytest

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session


from ..security.get_db import get_db
from .. import schemas


async def get_logged_user_override(cookie: str = "", db: Session = Depends(get_db)):
    # Return user openID
    return schemas.User(**{
        "id": 1,
        "externalId": "123",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "picture": "https://example.com/john.doe.jpg",
        "provider": "google",
        "language": "en",
        "darkMode": False,
    })


SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

def get_db_override():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

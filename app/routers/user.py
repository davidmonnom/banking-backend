from fastapi import Depends, HTTPException
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import schemas, utils
from ..security import get_logged_user, get_db


router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get(user: schemas.User = Depends(get_logged_user)) -> schemas.User:
    """Fetch the user's data."""
    return user


@router.put("/{user_id}")
async def update(user_id: int, data: schemas.UserUpdate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.User:
    """Update the user's preference."""
    if not user.id == user_id:
        raise HTTPException(status_code=400, detail="You can only update your own user")

    user = utils.user.update(db, user.id, user=schemas.UserUpdate(**{
        "language": data.language,
        "darkMode": data.darkMode
    }))

    return user


@router.post("/")
async def create(data: schemas.UserCreate,  user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.User:
    if not user.isAdmin == True:
        raise HTTPException(status_code=400, detail="You can only create users if you are an admin")

    user = utils.user.create(db, data)
    return user


@router.post("/shared/")
async def add_shared_user(email: str, db: Session = Depends(get_db), user: schemas.User = Depends(get_logged_user)) -> schemas.User:
    """Add a user to the shared group."""
    s_user = utils.user.get_by_email(db, email)

    if not s_user:
        raise HTTPException(status_code=400, detail="User not found")

    return utils.user.add_shared_user(db, user, s_user)


@router.delete("/shared/{user_id}")
async def remove_shared_user(user_id: int, db: Session = Depends(get_db), user: schemas.User = Depends(get_logged_user)) -> int:
    """Remove a user from the shared group."""
    s_user = utils.user.get(db, user_id)

    if not s_user:
        raise HTTPException(status_code=400, detail="User not found")

    return utils.user.delete_shared_user(db, user, s_user)

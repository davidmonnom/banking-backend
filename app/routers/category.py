from fastapi import Depends, HTTPException
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import utils, schemas
from ..security import get_logged_user, get_db


router = APIRouter(
    prefix="/category",
    tags=["Category"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def list(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> list[schemas.Category]:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    categories = utils.category.get_by_group_ids(db, group_ids)
    return categories


@router.post("/")
async def create(data: schemas.CategoryCreate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Category:
    if not data.groupId == user.ownedGroup[0].id:
        raise HTTPException(status_code=400, detail="You can only create categories for your own group")

    category = utils.category.create(db, data)
    return category


@router.put("/{category_id}")
async def update(category_id: int, data: schemas.CategoryCreate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Category:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    cat = utils.category.get_by_id(db, category_id)

    if not cat:
        raise HTTPException(status_code=400, detail="Category not found")

    if cat.groupId not in group_ids:
        raise HTTPException(status_code=400, detail="You can only update categories for your own group")

    category = utils.category.update(db, category_id, data)
    return category


@router.delete("/{category_id}")
async def delete(category_id: int, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> int:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    cat = utils.category.get_by_id(db, category_id)

    if not cat:
        raise HTTPException(status_code=400, detail="Category not found")

    if cat.groupId not in group_ids:
        raise HTTPException(status_code=400, detail="You can only delete categories for your own group")

    utils.category.delete(db, category_id)
    return category_id

import datetime

from fastapi import Depends, HTTPException
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import utils, schemas
from ..security import get_logged_user, get_db


router = APIRouter(
    prefix="/budget",
    tags=["Budget"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def list(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> list[schemas.Budget]:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    budgets = utils.budget.get_by_group_ids(db, group_ids)
    return budgets


@router.post("/")
async def create(data: schemas.BudgetCreate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Budget:
    if not data.groupId == user.ownedGroup[0].id:
        raise HTTPException(status_code=400, detail="You can only create categories for your own group")

    budget = utils.budget.create(db, data)
    return budget


@router.put("/{budget_id}")
async def update(budget_id: int, data: schemas.BudgetCreate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Budget:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    budget = utils.budget.get_by_id(db, budget_id)

    if not budget:
        raise HTTPException(status_code=400, detail="Budget not found")

    if not budget.groupId in group_ids:
        raise HTTPException(status_code=400, detail="You can only update budgets for your own group")

    budget = utils.budget.update(db, budget_id, data)
    return budget


@router.delete("/{budget_id}")
async def delete(budget_id: int, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> int:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    budget = utils.budget.get_by_id(db, budget_id)

    if not budget:
        raise HTTPException(status_code=400, detail="Budget not found")

    if not budget.groupId in group_ids:
        raise HTTPException(status_code=400, detail="You can only delete budgets for your own group")

    utils.budget.delete(db, budget_id)
    return budget_id

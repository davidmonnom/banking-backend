import datetime

from fastapi import Depends, HTTPException
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import utils, schemas
from ..security import get_logged_user, get_db


router = APIRouter(
    prefix="/goal",
    tags=["Goal"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def list(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> list[schemas.Goal]:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    goals = utils.goal.get_by_group_ids(db, group_ids)
    return goals


@router.post("/")
async def create(data: schemas.GoalCreate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Goal:
    if not data.groupId == user.ownedGroup[0].id:
        raise HTTPException(status_code=400, detail="You can only create categories for your own group")

    goal = utils.goal.create(db, data)
    return goal


@router.put("/{goal_id}")
async def update(goal_id: int, data: schemas.GoalCreate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Goal:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    goal = utils.goal.get_by_id(db, goal_id)

    if not goal:
        raise HTTPException(status_code=400, detail="Goal not found")

    if not goal.groupId in group_ids:
        raise HTTPException(status_code=400, detail="You can only update goals for your own group")

    goal = utils.goal.update(db, goal_id, data)
    return goal


@router.delete("/{goal_id}")
async def delete(goal_id: int, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> int:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    goal = utils.goal.get_by_id(db, goal_id)

    if not goal:
        raise HTTPException(status_code=400, detail="Goal not found")

    if not goal.groupId in group_ids:
        raise HTTPException(status_code=400, detail="You can only delete goals for your own group")

    utils.goal.delete(db, goal_id)
    return goal_id

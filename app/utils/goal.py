from sqlalchemy.orm import Session
from .. import models, schemas


def get_by_id(db: Session, goal_id: int):
    return db.query(models.Goal).filter(models.Goal.id == goal_id).first()


def get_by_group_ids(db: Session, group_ids: list):
    return db.query(models.Goal).filter(models.Goal.groupId.in_(group_ids)).all()


def create(db: Session, goal: schemas.GoalCreate):
    db_goal = models.Goal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def update(db: Session, goal_id: int, goal: schemas.GoalCreate):
    db_goal = db.query(models.Goal).filter(
        models.Goal.id == goal_id).first()

    for var, value in goal.model_dump().items():
        setattr(db_goal, var, value)

    db.commit()
    db.refresh(db_goal)
    return db_goal


def delete(db: Session, goal_id: int):
    db.query(models.Goal).filter(models.Goal.id == goal_id).delete()
    db.commit()
    return goal_id

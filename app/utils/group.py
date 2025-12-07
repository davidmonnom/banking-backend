from sqlalchemy.orm import Session
from .. import models, schemas


def get(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def create(db: Session, group: schemas.GroupCreate):
    db_group = models.Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def update(db: Session, group_id: int, group: schemas.GroupCreate):
    db_group = db.query(models.Group).filter(
        models.Group.id == group_id).first()
    db_group.update(**group.model_dump())
    db.commit()
    db.refresh(db_group)
    return db_group


def delete(db: Session, group_id: int):
    db.query(models.Group).filter(models.Group.id == group_id).delete()
    db.commit()
    return group_id

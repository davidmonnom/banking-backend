from sqlalchemy.orm import Session
from .. import models, schemas


def get(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_by_group_ids(db: Session, group_ids: list):
    return db.query(models.Item).filter(models.Item.groupId.in_(group_ids)).all()


def create(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(
        models.Item.id == item_id).first()

    for var, value in item.model_dump().items():
        setattr(db_item, var, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete(db: Session, item_id: int):
    db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()
    return item_id

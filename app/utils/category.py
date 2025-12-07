from sqlalchemy.orm import Session
from .. import models, schemas


def get_by_id(db: Session, category_id: int) -> models.Category:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_by_group_ids(db: Session, group_ids: list) -> list[models.Category]:
    return db.query(models.Category).filter(models.Category.groupId.in_(group_ids)).all()


def create(db: Session, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update(db: Session, category_id: int, category: schemas.CategoryCreate) -> models.Category:
    db_category = db.query(models.Category).filter(
        models.Category.id == category_id).first()

    for var, value in category.model_dump().items():
        setattr(db_category, var, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete(db: Session, category_id: int) -> int:
    db.query(models.Category).filter(
        models.Category.id == category_id).delete()
    db.commit()
    return category_id

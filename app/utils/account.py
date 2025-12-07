from sqlalchemy.orm import Session
from .. import models, schemas


def get(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()


def get_by_group_ids(db: Session, group_ids: list):
    return db.query(models.Account).filter(models.Account.groupId.in_(group_ids)).all()


def create(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def update(db: Session, account_id: int, account: schemas.AccountUpdate):
    db_account = db.query(models.Account).filter(
        models.Account.id == account_id).first()

    for var, value in account.model_dump().items():
        setattr(db_account, var, value)

    db.commit()
    db.refresh(db_account)
    return db_account


def delete(db: Session, account_id: int):
    db.query(models.Account).filter(models.Account.id == account_id).delete()
    db.commit()
    return account_id

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import text

from .. import models, schemas


def get_by_id(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()


def get_between_dates(db: Session, date_start: str, date_end: str, account_ids: list[int]):
    # get all transactions and ids of relations
    return db.query(models.Transaction).filter(
        models.Transaction.date >= date_start,
        models.Transaction.date <= date_end,
        models.Transaction.accountId.in_(account_ids)
    ).all()


def create_many(db: Session, transactions: list[schemas.TransactionCreate]):
    operations = [insert(models.Transaction).values(**transaction.model_dump()).on_conflict_do_nothing() for transaction in transactions]
    for operation in operations:
        db.execute(operation)
    db.commit()
    return True


def update(db: Session, transaction_id: int, data: schemas.TransactionUpdate):
    relations = {
        "categories": models.Category,
        "goals": models.Goal,
        "budgets": models.Budget
    }

    db_transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id).first()

    for var, value in data.model_dump().items():
        if hasattr(db_transaction, var) and var not in relations:
            setattr(db_transaction, var, value)
        elif hasattr(db_transaction, var) and var in relations:
            model = relations[var]
            record = [db.query(model).filter(model.id == item_id).first() for item_id in value]
            setattr(db_transaction, var, record)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete(db: Session, transaction_id: int):
    db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id).delete()
    db.commit()
    return transaction_id

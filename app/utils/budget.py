from sqlalchemy.orm import Session
from .. import models, schemas


def get_by_id(db: Session, budget_id: int) -> models.Budget:
    return db.query(models.Budget).filter(models.Budget.id == budget_id).first()


def get_by_group_ids(db: Session, group_ids: list) -> list[models.Budget]:
    return db.query(models.Budget).filter(models.Budget.groupId.in_(group_ids)).all()


def create(db: Session, budget: schemas.BudgetCreate) -> models.Budget:
    db_budget = models.Budget(**budget.model_dump())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def update(db: Session, budget_id: int, budget: schemas.BudgetCreate) -> models.Budget:
    db_budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id).first()

    for var, value in budget.model_dump().items():
        setattr(db_budget, var, value)

    db.commit()
    db.refresh(db_budget)
    return db_budget


def delete(db: Session, budget_id: int) -> int:
    db.query(models.Budget).filter(models.Budget.id == budget_id).delete()
    db.commit()
    return budget_id

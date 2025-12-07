from sqlalchemy.orm import Session
from .. import models, schemas


def get(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_by_external_id(db: Session, external_id: str):
    return db.query(models.User).filter(models.User.externalId == external_id).first()


def get_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_shared_users(db: Session, groups: list[models.Group]):
    users = db.query(models.User).all()
    valid_users = []

    for user in users:
        if user.groups in groups:
            valid_users.append(user)

    return valid_users


def add_shared_user(db: Session, user: models.User, s_user: models.User):
    owner_group = user.ownedGroup[0]
    s_user.groups.append(owner_group)
    db.commit()
    db.refresh(s_user)
    return s_user


def delete_shared_user(db: Session, user: models.User, s_user: models.User):
    # TODO delete all related relations between unaccessible records
    owner_group = user.ownedGroup[0]
    s_user.groups.remove(owner_group)
    db.commit()
    db.refresh(s_user)
    return s_user.id


def create(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(
        models.User.id == user_id).first()

    for var, value in user.model_dump().items():
        setattr(db_user, var, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return user_id

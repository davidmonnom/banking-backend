from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import utils, schemas
from ..plaid import token
from ..security import get_logged_user, get_db


router = APIRouter(
    prefix="/data",
    tags=["Data"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/init")
async def init(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)):
    """Fetch initial data for the user."""
    group_ids = list(
        set([group.id for group in user.groups + user.ownedGroup]))

    items = utils.item.get_by_group_ids(db, group_ids)
    accounts = utils.account.get_by_group_ids(db, group_ids)
    categories = utils.category.get_by_group_ids(db, group_ids)
    budgets = utils.budget.get_by_group_ids(db, group_ids)
    goals = utils.goal.get_by_group_ids(db, group_ids)
    sharedUsers = utils.user.get_shared_users(db, user.ownedGroup)

    return {
        "user": user,
        "sharedUsers": sharedUsers,
        "items": items,
        "accounts": accounts,
        "categories": categories,
        "budgets": budgets,
        "goals": goals
    }


# Let's separate the link from the init endpoint
@router.get("/link")
async def link_token(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)):
    """Fetch a new link token for the user."""
    link = token.get_token()
    if not link:
        return {"error": "Failed to create link token."}
    return {"linkToken": link.link_token}

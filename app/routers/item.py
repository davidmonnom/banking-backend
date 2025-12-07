from fastapi import Depends, HTTPException
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import utils, schemas
from ..plaid import token, get_item, get_institution, get_account
from ..security import get_logged_user, get_db


router = APIRouter(
    prefix="/item",
    tags=["Item"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def list(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> list[schemas.Item]:
    group_ids = [group.id for group in user.groups + user.ownedGroup]
    items = utils.item.get_by_group_ids(db, group_ids)

    # Delete sensitive data
    for item in items:
        item.accessToken = "sensitive data"
        item.publicToken = "sensitive data"
        item.itemId = "sensitive data"

    return items



@router.post("/")
async def create(public_token: str, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Item:
    """Create a new item."""

    try:
        plaid_access_token = token.post_token(public_token)
        plaid_item = get_item(plaid_access_token.access_token)
        plaid_institution = get_institution("ins_133650")
        plaid_accounts = get_account(plaid_access_token.access_token)
    except Exception as error:
        raise HTTPException(
            status_code=500, detail="Plaid error") from error

    try:
        item = utils.item.create(db, schemas.ItemCreate(**{
            "publicToken": public_token,
            "accessToken": plaid_access_token.access_token,
            "itemId": plaid_item.item.item_id,
            "institutionId": plaid_item.item.institution_id,
            "institutionName": plaid_institution["institution"]['name'],
            "webhook": "",
            "userId": user.id,
            "groupId": user.ownedGroup[0].id,
            "expirationDate": plaid_item.item.consent_expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
        }))

        for account in plaid_accounts.accounts:
            utils.account.create(db, schemas.AccountCreate(**{
                "name": account.name,
                "accountId": account.account_id,
                "mask": account.mask,
                "officialName": account.official_name,
                "type": account.type.value,
                "subtype": account.subtype.value,
                "balances": account.balances.current,
                "groupId": user.ownedGroup[0].id,
                "itemId": item.id,
                "transactions": [],
            }))
    except Exception as error:
        if error.orig.pgcode == '23505':
            raise HTTPException(
                status_code=500, detail="Item already exists") from error
        else:
            raise HTTPException(
                status_code=500, detail="Server error") from error

    return item

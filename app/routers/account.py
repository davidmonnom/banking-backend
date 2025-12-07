import os

from fastapi import Depends
from fastapi_sso.sso.base import OpenID
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import utils, schemas
from ..plaid import token, get_account
from ..security import get_logged_user, get_db

router = APIRouter(
    prefix="/account",
    tags=["Account"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/sync")
async def sync(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)):
    group_ids = list(
        set([group.id for group in user.groups + user.ownedGroup]))
    user_item = utils.item.get_by_group_ids(db, group_ids)
    accounts = utils.account.get_by_group_ids(db, group_ids)

    for item in user_item:
        plaid_accounts = get_account(item.accessToken)

        for new_account in plaid_accounts.accounts:
            if new_account.account_id in [account.accountId for account in accounts]:
                account = [
                    account for account in accounts if account.accountId == new_account.account_id][0]

                utils.account.update(db, account.id, schemas.AccountUpdate(**{
                    "name": new_account.name,
                    "balances": new_account.balances.current,
                }))

                continue

            account = utils.account.create(db, schemas.AccountCreate(**{
                "name": new_account.name,
                "accountId": new_account.account_id,
                "mask": new_account.mask,
                "officialName": new_account.official_name,
                "type": new_account.type.value,
                "subtype": new_account.subtype.value,
                "balances": new_account.balances.current,
                "groupId": user.ownedGroup[0].id,
                "itemId": item.id,
                "transactions": [],
            }))

            accounts.append(account)

    return utils.account.get_by_group_ids(db, group_ids)

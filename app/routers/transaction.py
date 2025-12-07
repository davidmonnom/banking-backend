import datetime

from fastapi import Depends, HTTPException, Response
from fastapi import APIRouter

from sqlalchemy.orm import Session

from .. import utils, schemas
from ..plaid import sync_transactions
from ..security import get_logged_user, get_db


router = APIRouter(
    prefix="/transaction",
    tags=["Transaction"],
    dependencies=[Depends(get_logged_user)],
    responses={404: {"description": "Not found"}},
    route_class=utils.timed.Route
)


@router.get("/list")
async def list(date_start: str = "", date_end: str = "",user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> list[schemas.Transaction]:
    group_ids =  [group.id for group in user.groups + user.ownedGroup]
    account_ids = [account.id for account in utils.account.get_by_group_ids(db, group_ids)]
    transactions = utils.transaction.get_between_dates(db, date_start, date_end, account_ids)
    return transactions


@router.get("/sync")
async def sync(user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)):
    transactions = {}
    group_ids =  [group.id for group in user.groups + user.ownedGroup]
    user_item = utils.item.get_by_group_ids(db, group_ids)
    user_account = utils.account.get_by_group_ids(db, group_ids)
    account_by_ext_id = {account.accountId: account for account in user_account}

    for item in user_item:
        transactions = sync_transactions(item)

        if transactions.get('added') and len(transactions.get('added')) > 0:
            transaction_to_add = []

            for transaction in transactions.added:
                transaction_to_add.append(schemas.TransactionCreate(**{
                    "accountId": account_by_ext_id[transaction.account_id].id,
                    "transactionId": transaction.transaction_id,
                    "amount": -float(transaction.amount),
                    "name": transaction.name,
                    "merchantName": transaction.merchant_name,
                    "merchantEntityId": transaction.merchant_entity_id,
                    "date": transaction.date.strftime("%Y-%m-%d %H:%M:%S"),
                    "isoCurrencyCode": transaction.iso_currency_code,
                }))

            utils.transaction.create_many(db, transaction_to_add)
            utils.item.update(db, item.id, schemas.ItemUpdate(**{
                "updateDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "cursor": transactions.next_cursor
            }))

    return {
        "status": "success",
        "message": "Transactions synced successfully",
        "details": {
            "added": len(transactions.get('added')) if transactions.get('added') else 0,
            "has_more": transactions.get('has_more') or False,
        }
    }


@router.put("/{transaction_id}")
async def update(transaction_id: int, data: schemas.TransactionUpdate, user: schemas.User = Depends(get_logged_user), db: Session = Depends(get_db)) -> schemas.Transaction:
    group_ids =  [group.id for group in user.groups + user.ownedGroup]
    account_ids = [account.id for account in utils.account.get_by_group_ids(db, group_ids)]
    transaction = utils.transaction.get_by_id(db, transaction_id)

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if transaction.accountId not in account_ids:
        raise HTTPException(status_code=403, detail="Forbidden")

    transaction = utils.transaction.update(db, transaction.id, data=schemas.TransactionUpdate(**{
        "name": data.name or transaction.name,
        "merchantName": data.merchantName or transaction.merchantName,
        "merchantWebsite": data.merchantWebsite or transaction.merchantWebsite,
        "merchantEntityId": data.merchantEntityId or transaction.merchantEntityId,
        "categories": data.categories,
        "goals": data.goals,
        "budgets": data.budgets,
    }))

    return transaction

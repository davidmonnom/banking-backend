from plaid.model.transactions_sync_request import TransactionsSyncRequest

from ..security import get_plaid_client


def sync_transactions(item):
    client = get_plaid_client()

    transaction_sync_request = TransactionsSyncRequest(
        access_token=item.accessToken,
        cursor=item.cursor or "",
        count=50,
    )

    return client.transactions_sync(transaction_sync_request)

from plaid.model.accounts_get_request import AccountsGetRequest

from ..security import get_plaid_client


def get_account(access_token: str):
    client = get_plaid_client()
    account_request = AccountsGetRequest(access_token=access_token)
    return client.accounts_get(account_request)

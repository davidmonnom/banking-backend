from plaid.model.item_get_request import ItemGetRequest

from ..security import get_plaid_client


def get_item(access_token: str):
    client = get_plaid_client()
    item_request = ItemGetRequest(access_token=access_token)
    return client.item_get(item_request)

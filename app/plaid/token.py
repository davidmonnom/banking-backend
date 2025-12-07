import time
import traceback
import logging

from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from ..security import get_plaid_client


def get_token():
    client = get_plaid_client()

    try:
        request = LinkTokenCreateRequest(
            products=[Products("auth"), Products("transactions")],
            client_name="Cedav Finance",
            country_codes=[CountryCode("BE")],
            language="en",
            user=LinkTokenCreateRequestUser(client_user_id=str(time.time())),
        )
    except Exception as e:
        logging.error(traceback.format_exc())
        return False

    return client.link_token_create(request)


def post_token(public_token: str):
    client = get_plaid_client()
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    exchange_response = client.item_public_token_exchange(exchange_request)
    return exchange_response

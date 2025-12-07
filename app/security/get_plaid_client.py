import os

import plaid
from plaid.api import plaid_api

PLAID_CLIENT_ID = os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET = os.environ.get('PLAID_SECRET')

def get_plaid_client():
    '''Create a new client for testing.'''
    configuration = plaid.Configuration(
        host=plaid.Environment.Production,
        api_key={
            'clientId': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
        }
    )


    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

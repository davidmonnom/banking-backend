from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.country_code import CountryCode

from ..security import get_plaid_client


def get_institution(institution_id: str):
    client = get_plaid_client()
    institution_request = InstitutionsGetByIdRequest(
        institution_id=institution_id,  country_codes=[CountryCode("BE")])
    return client.institutions_get_by_id(institution_request)

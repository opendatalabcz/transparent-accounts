from flask import Blueprint
from flask_restx import Api

from app.apis.account import api as account_api
from app.apis.bank import api as bank_api
from app.apis.occurrence import api as occurrence_api
from app.apis.transaction import api as transaction_api
from app.apis.update import api as update_api

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title='Transparent accounts API',
    version='1.0',
    description="""
    API for transparent accounts.
    The API allows you to search for accounts and transactions, update accounts and search for occurrences of identifiers or counter accounts in accounts transactions.
    """
)

api.add_namespace(bank_api)
api.add_namespace(account_api)
api.add_namespace(transaction_api, path='/accounts')
api.add_namespace(update_api, path='/accounts')
api.add_namespace(occurrence_api)

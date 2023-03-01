from flask import request
from flask_restx import Namespace, Resource, fields

from app.models import Bank
from app.queries import find_accounts, find_account
from app.utils import generalize_query

api = Namespace('accounts', description='Access to the accounts')

account_model = api.model(
    'Account',
    {
        'number': fields.String(required=True, example='000000-2902252345', description='The account number without bank code in fully qualified format - six digits prefix, a hyphen and ten digits number'),
        'bank_code': fields.String(attribute=lambda x: x.bank.value, required=True, example='2010', description='The account bank code - four digits number'),
        'name': fields.String(required=True, example='generalpavel', description='The account name (may be null if not fetched yet)'),
        'owner': fields.String(required=True, example='Ing. Pavel, Petr', description='The account owner'),
        'balance': fields.Float(required=True, example=2782489.38, description='The account current balance (may be null if not fetched yet)'),
        'currency': fields.String(required=True, example='CZK', description='The account currency (may be null if not fetched yet)'),
        'description': fields.String(required=True, example='https://www.generalpavel.cz/', description='The account description, supported only by a few banks'),
        'created': fields.Date(required=True, example='2023-07-01', description='The date of account creation, supported only by a few banks'),
        'last_updated': fields.DateTime(required=True, example='2023-03-01T03:00:00.000000', description='The date of last account update, accounts are updated automatically every 24 hours'),
        'last_fetched': fields.DateTime(required=True, example='2023-03-01T09:15:13.426125', description='The date of last account fetch, accounts details and transactions are fetched on demand'),
        'archived': fields.Boolean(required=True, example=False, description='Flag if the account is still active and can be found on the banks website'),
    },
)


@api.route('/')
class AccountList(Resource):
    @api.doc('list_accounts')
    @api.param('query', 'Search for accounts with name, owner or number containing the query string', 'query')
    @api.param('limit', 'Limit the number of returned accounts', 'query')
    @api.param('order_by', 'Order the results by either "number" or "last_fetched"', 'query')
    @api.marshal_list_with(account_model)
    def get(self):
        """
        List all accounts.
        Various query parameters can be used to filter the results.
        """
        # Get and generalize query, so that it can be used more broadly
        query = request.args.get('query')
        query = generalize_query(query)
        # Get limit and convert it to int or None (meaning no limit)
        limit = request.args.get('limit')
        limit = int(limit) if limit and limit.isdigit() else None
        # Only allow ordering by 'last_fetched' if requested, otherwise order by 'number'
        order_by = 'last_fetched' if request.args.get('order_by') == 'last_fetched' else 'number'

        accounts = find_accounts(query, limit, order_by)

        return accounts


@api.route('/<bank_code>/<acc_num>')
@api.param('bank_code', 'The account bank code')
@api.param('acc_num', 'The account number')
@api.response(400, 'Bank not supported')
@api.response(404, 'Account not found')
class Account(Resource):
    @api.doc('get_account')
    @api.marshal_with(account_model)
    def get(self, bank_code: str, acc_num: str):
        """
        Fetch an account specified by its number and bank code.
        """
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')

        account = find_account(acc_num, bank)

        if account is None:
            api.abort(404, 'Account not found')

        return account

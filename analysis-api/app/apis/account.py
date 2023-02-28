from flask import request
from flask_restx import Namespace, Resource, fields

from app.models import Bank
from app.queries import find_accounts, find_account
from app.utils import generalize_query

api = Namespace('accounts', description='Accounts related operations')

account_model = api.model(
    'Account',
    {
        'number': fields.String(required=True, description='The bank shortcut'),
        'bank_code': fields.String(attribute=lambda x: x.bank.value, required=True, description='The bank shortcut'),
        'name': fields.String(required=True, description='The bank shortcut'),
        'owner': fields.String(required=True, description='The bank shortcut'),
        'balance': fields.Float(required=True, description='The bank shortcut'),
        'currency': fields.String(required=True, description='The bank shortcut'),
        'description': fields.String(required=True, description='The bank shortcut'),
        'created': fields.Date(required=True, description='The bank shortcut'),
        'last_updated': fields.DateTime(required=True, description='The bank shortcut'),
        'last_fetched': fields.DateTime(required=True, description='The bank shortcut'),
        'archived': fields.Boolean(required=True, description='The bank shortcut'),
    },
)


@api.route('/')
class AccountList(Resource):
    @api.doc('list_accounts')
    @api.marshal_list_with(account_model)
    def get(self):
        """List all accounts"""
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


@api.route("/<bank_code>/<acc_num>")
@api.param("bank_code", "The account bank code")
@api.param("acc_num", "The account number")
@api.response(400, "Bank not supported")
@api.response(404, "Account not found")
class Account(Resource):
    @api.doc("get_account")
    @api.marshal_with(account_model)
    def get(self, bank_code: str, acc_num: str):
        """Fetch an account given its number and bank code"""
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')

        account = find_account(acc_num, bank)

        if account is None:
            api.abort(404, 'Account not found')

        return account

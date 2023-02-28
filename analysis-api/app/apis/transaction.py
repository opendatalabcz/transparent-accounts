from flask_restx import Namespace, Resource, fields

from app.models import Bank
from app.queries import find_account, find_transactions

api = Namespace('transactions', description='Transactions related operations')

transaction_model = api.model(
    'Transaction',
    {
        'id': fields.Integer(required=True, description='The transaction id'),
        'date': fields.Date(required=True, description='The transaction date'),
        'amount': fields.Float(required=True, description='The transaction amount'),
        'currency': fields.String(required=True, description='The transaction currency'),
        'counter_account': fields.String(required=True, description='The transaction counter account'),
        'type': fields.String(attribute=lambda x: x.type.name, required=True, description='The transaction type'),
        'type_detail': fields.String(required=True, description='The transaction detail type'),
        'variable_symbol': fields.String(required=True, description='The transaction variable symbol'),
        'constant_symbol': fields.String(required=True, description='The transaction constant symbol'),
        'specific_symbol': fields.String(required=True, description='The transaction specific symbol'),
        'description': fields.String(required=True, description='The transaction description'),
        'ca_identifier': fields.String(required=True, description='The transaction counter account identifier'),
        'ca_name': fields.String(required=True, description='The transaction counter account company name'),
        'category': fields.String(required=True, description='The transaction category'),
    }
)


@api.route("/<bank_code>/<acc_num>/transactions")
@api.param("bank_code", "The account bank code")
@api.param("acc_num", "The account number")
@api.response(400, "Bank not supported")
@api.response(404, "Account not found")
class TransactionList(Resource):
    @api.doc("list_transactions")
    @api.marshal_with(transaction_model)
    def get(self, bank_code: str, acc_num: str):
        """Fetch an account given its number and bank code"""
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')

        account = find_account(acc_num, bank)

        if account is None:
            api.abort(404, 'Account not found')

        transactions = find_transactions(acc_num, bank)
        return transactions

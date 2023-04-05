from flask_restx import Namespace, Resource, fields

from app.models import Bank
from app.queries import find_account, find_transactions

api = Namespace('transactions', description='Access to transactions of the accounts')

transaction_model = api.model(
    'Transaction',
    {
        'id': fields.Integer(required=True, example=1, description='The transaction id - artificial identifier unique within the transactions'),
        'date': fields.Date(required=True, example='2023-03-01', description='The date the transaction was sent/credited'),
        'amount': fields.Float(required=True, example=-2500.25, description='The transaction amount'),
        'currency': fields.String(required=True, example='CZK', description='The transaction currency'),
        'counter_account': fields.String(required=True, example='Jakub Janeček', description='The transaction counter account, may be unknown - null'),
        'type': fields.String(attribute=lambda x: x.type.name, example='OUTGOING', required=True, description='The transaction type, either INCOMING or OUTGOING'),
        'typ_detail': fields.String(attribute=lambda x: x.type_detail.name, required=True, example='Výběr z bankomatu', description='The transaction detail type, this type is determined from the other attributes'),
        'type_str': fields.String(required=True, example='Okamžitá odchozí platba', description='The transaction type, this type is provided by the bank and may be different for each bank'),
        'variable_symbol': fields.String(required=True, example='20230001', description='The transaction variable symbol'),
        'constant_symbol': fields.String(required=True, example='', description='The transaction constant symbol'),
        'specific_symbol': fields.String(required=True, example='', description='The transaction specific symbol'),
        'description': fields.String(required=True, example='Testovaci transakce, IČO: 04434081', description='The transaction description, may be empty'),
        'ca_identifier': fields.String(required=True, example='04434081', description='The transaction counter account identifier parsed from the description'),
        'ca_name': fields.String(required=True, example='Profinit EU, s.r.o.', description='The transaction counter account company name, fetched from the https://www.mfcr.cz/ using identifier'),
        'category': fields.String(required=True, example='Marketing', description='The transaction recognized category'),
    }
)


@api.route('/<bank_code>/<acc_num>/transactions')
@api.param('bank_code', 'The account bank code')
@api.param('acc_num', 'The account number')
@api.response(400, 'Bank not supported')
@api.response(404, 'Account not found')
class TransactionList(Resource):
    @api.doc('list_transactions')
    @api.marshal_with(transaction_model)
    def get(self, bank_code: str, acc_num: str):
        """
        Get transactions of an account specified by its number and bank code.
        """
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')

        account = find_account(acc_num, bank)

        if account is None:
            api.abort(404, 'Account not found')

        transactions = find_transactions(acc_num, bank)
        return transactions

from flask_restx import Namespace, Resource, fields

from app import banks
from app.models import Bank
from app.queries import get_accounts_count

api = Namespace('banks', description='Banks related operations')

account_model = api.model(
    'Bank',
    {
        'shortcut': fields.String(required=True, description='The bank shortcut'),
        'name': fields.String(required=True, description='The bank name'),
        'url': fields.String(required=True, description='The bank website'),
        'code': fields.String(required=True, description='The bank code'),
        'accounts_count': fields.Integer(required=True, description='Number of transparent accounts managed by the bank'),
    },
)


@api.route('/')
class OccurrenceList(Resource):
    @api.doc('list_banks')
    @api.marshal_list_with(account_model)
    def get(self):
        """List all banks"""
        # Get banks from config and calculate the number of accounts for each bank
        for bank in banks:
            bank['accounts_count'] = get_accounts_count(Bank(bank['code']))

        # Filter out not supported banks (banks with 0 accounts)
        filtered_banks = list(filter(lambda b: b['accounts_count'] > 0, banks))

        return filtered_banks

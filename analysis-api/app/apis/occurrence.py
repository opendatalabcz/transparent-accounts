from flask import request
from flask_restx import Namespace, Resource

from app.apis.account import account_model
from app.queries import find_accounts_by_identifier_occurrence, find_accounts_by_counter_account_occurrence

api = Namespace('occurrences', description='Access to accounts by occurrences of identifiers or counter accounts in their transactions')


@api.route('/')
@api.param('identifier', 'The identifier to look for in transactions', 'query')
@api.param('counter_account', 'The counter account to look for in transactions', 'query')
@api.response(400, 'Exactly one of the identifier or counter_account query parameters must be specified')
class Occurrence(Resource):
    @api.doc('list_occurrences')
    @api.marshal_list_with(account_model)
    def get(self):
        """
        List all accounts occurrences.
        This endpoint returns such accounts in whose transactions the given identifier or counter_account occurred at least once.
        Exactly one of the identifier or counter_account query parameters must be specified.
        """
        identifier = request.args.get('identifier')
        counter_account = request.args.get('counter_account')

        # Exactly one of identifier or counter_account parameter must be specified
        if (identifier is None and counter_account is None) or (identifier is not None and counter_account is not None):
            api.abort(400, 'Exactly one of the identifier or counter_account query parameters must be specified')

        if identifier is not None:
            occurrences = find_accounts_by_identifier_occurrence(identifier)
        elif counter_account is not None:
            occurrences = find_accounts_by_counter_account_occurrence(counter_account)

        return occurrences

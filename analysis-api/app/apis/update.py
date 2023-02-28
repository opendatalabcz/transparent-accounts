from datetime import datetime
from flask_restx import Namespace, Resource, fields

from app import celery
from app.models import Bank, AccountUpdate, UpdateStatus
from app.queries import find_account, find_updates, save_update, find_update
from app.utils import is_updatable

api = Namespace('updates', description='Accounts related operations')

update_model = api.model(
    'Update',
    {
        'id': fields.Integer(required=True, description='The update id'),
        'status': fields.String(attribute=lambda x: x.status.name, required=True, description='The bank shortcut'),
        'started': fields.DateTime(required=True, description='The transaction date'),
        'ended': fields.DateTime(required=True, description='The transaction date'),
        'account_number': fields.String(required=True, description='The bank shortcut'),
        'account_bank': fields.String(attribute=lambda x: x.bank.value, required=True, description='The bank shortcut'),
    }
)

status_model = api.model(
    'Status',
    {
        'status': fields.String(required=True, description='The bank shortcut'),
        'updatable': fields.Boolean(required=True, description='The bank shortcut'),
    },
)


@api.route("/<bank_code>/<acc_num>/updates")
@api.param("bank_code", "The account bank code")
@api.param("acc_num", "The account number")
@api.response(400, "Bank not supported or account not updatable")
@api.response(404, "Account not found")
class UpdateList(Resource):
    @api.doc("list_updates")
    @api.marshal_with(update_model)
    def get(self, bank_code: str, acc_num: str):
        """List all updates"""
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')

        account = find_account(acc_num, bank)

        if account is None:
            api.abort(404, 'Account not found')

        updates = find_updates(acc_num, bank)

        return updates

    @api.doc("post_update")
    @api.marshal_with(update_model)
    def post(self, bank_code: str, acc_num: str):
        """Post update"""
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')
        account = find_account(acc_num, bank)
        if account is None:
            api.abort(404, 'Account not found')

        # Check if the account is updatable
        if not is_updatable(account):
            api.abort(400, 'Account is not updatable')

        # Create a new update request, save it to the database and send a task using Celery
        account_request = AccountUpdate(account_number=account.number, account_bank=account.bank,
                                        status=UpdateStatus.PENDING, started=datetime.now())
        save_update(account_request)
        try:
            celery.send_task('app.tasks.fetch_transactions', args=[account_request.id])
        except Exception:
            api.abort(500, 'Service unavailable')

        return 202, {'Location': f"/accounts/{bank_code}/{acc_num}/updates/{account_request.id}"}


@api.route("/<bank_code>/<acc_num>/updates/<int:update_id>")
@api.param("bank_code", "The account bank code")
@api.param("acc_num", "The account number")
@api.param("update_id", "The update id")
@api.response(400, "Bank not supported")
@api.response(404, "Update not found")
class Update(Resource):
    @api.doc("get_update")
    @api.marshal_with(update_model)
    def get(self, bank_code: str, acc_num: str, update_id: int):
        """Fetch an update given its bank code, account number and id"""
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')

        update = find_update(update_id)

        # Update not found or the update's account or bank differs from the requested one
        if update is None or update.account_bank != bank or update.account_number != acc_num:
            api.abort(404, 'Update not found')

        return update


@api.route("/<bank_code>/<acc_num>/status")
@api.param("bank_code", "The account bank code")
@api.param("acc_num", "The account number")
@api.param("update_id", "The update id")
@api.response(400, "Bank not supported")
@api.response(404, "Account not found")
class Status(Resource):
    @api.doc("get_status")
    @api.marshal_with(status_model)
    def get(self, bank_code: str, acc_num: str):
        """"""
        try:
            bank = Bank(bank_code)
        except ValueError:
            api.abort(400, 'Bank not supported')

        account = find_account(acc_num, bank)

        if account is None:
            api.abort(404, 'Account not found')

        # Get the last update and check if the account is updatable
        updates = find_updates(acc_num, bank)
        last_update_status = updates[0].status.name if len(updates) > 0 else None
        updatable = is_updatable(account)

        return {'status': last_update_status, 'updatable': updatable}

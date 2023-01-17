import json

from flask import request

from app import app, celery, bp
from app.models import Bank, AccountUpdate, UpdateStatus
from app.queries import find_account, find_accounts, find_update, save_update
from app.utils import object_encode, generalize_query


@bp.get("/accounts")
def get_accounts():
    query = request.args.get('query')
    query = generalize_query(query)
    accounts = find_accounts(query)
    response = app.response_class(
        response=json.dumps(accounts, default=object_encode),
        mimetype='application/json'
    )
    return response


@bp.get("/accounts/<bank_code>/<acc_num>")
def get_account(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return  # TODO

    account = find_account(acc_num, bank)

    if account is None:
        return  # TODO

    response = app.response_class(
        response=json.dumps(account, default=object_encode),
        mimetype='application/json'
    )
    return response


@bp.post("/accounts/<bank_code>/<acc_num>/updates")
def fetch_transactions(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return  # TODO

    account = find_account(acc_num, bank)

    if account is None:
        return  # TODO

    account_request = AccountUpdate(account_number=account.number, account_bank=account.bank)
    save_update(account_request, UpdateStatus.PENDING)
    celery.send_task('app.tasks.fetch_transactions', args=[account_request.id])

    response = app.response_class(
        status=202,
    )
    response.headers['Location'] = f"/accounts/{bank_code}/{acc_num}/updates/{account_request.id}"

    return response


@bp.get("/accounts/<bank_code>/<acc_num>/updates/<update_id>")
def get_update(bank_code: str, acc_num: str, update_id: int):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return   # TODO

    update = find_update(update_id)

    if update is None or update.account_bank != bank or update.account_number != acc_num:
        return  # TODO

    response = app.response_class(
        response=json.dumps(update, default=str),
        mimetype='application/json'
    )
    return response


@bp.get("/admin/accounts/<bank_code>")
def fetch_accounts(bank_code):
    celery.send_task('app.tasks.fetch_accounts', args=[bank_code])
    return 202

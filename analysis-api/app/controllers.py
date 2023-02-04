import json
from datetime import datetime

from flask import request

from app import app, celery, bp
from app.models import Bank, AccountUpdate, UpdateStatus
from app.queries import find_account, find_transactions, find_accounts, find_update, save_update
from app.fetchers import fetch_identifier
from app.utils import object_encode, generalize_query


@bp.get("/accounts")
def get_accounts():
    query = request.args.get('query')
    query = generalize_query(query)
    limit = request.args.get('limit')
    limit = int(limit) if limit and limit.isdigit() else None
    order_by = 'last_fetched' if request.args.get('order_by') == 'last_fetched' else None

    accounts = find_accounts(query, limit, order_by)
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


@bp.get("/accounts/<bank_code>/<acc_num>/transactions")
def get_transactions(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return  # TODO

    account = find_account(acc_num, bank)

    if account is None:
        return  # TODO

    transactions = find_transactions(acc_num, bank)

    response = app.response_class(
        response=json.dumps(transactions, default=object_encode),
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

    account_request = AccountUpdate(account_number=account.number, account_bank=account.bank,
                                    status=UpdateStatus.PENDING, started=datetime.now())
    save_update(account_request)
    celery.send_task('app.tasks.fetch_transactions', args=[account_request.id])

    response = app.response_class(
        status=202,
    )
    response.headers['Location'] = f"/accounts/{bank_code}/{acc_num}/updates/{account_request.id}"

    return response


@bp.get("/accounts/<bank_code>/<acc_num>/updates")
def get_updates(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return

    # TODO implement real solution
    response = app.response_class(
        response=json.dumps({"updates": [], "updatable": True}),
        mimetype='application/json'
    )
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


@bp.get("/identifiers/<identifier>")
def get_identifier(identifier: str):
    name = fetch_identifier(identifier)
    response = app.response_class(
        response=json.dumps({"identifier": identifier, "name": name}),
        mimetype='application/json'
    )
    return response


#  TODO temporary, remove in production
@bp.get("/admin/accounts/<bank_code>")
def fetch_accounts(bank_code):
    celery.send_task('app.tasks.fetch_accounts', args=[bank_code])
    return 202

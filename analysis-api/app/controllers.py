import json
from datetime import datetime

from flask import request

from app import app, celery, bp
from app.models import Bank, AccountUpdate, UpdateStatus
from app.queries import find_account, find_transactions, find_accounts, find_update, save_update
from app.fetchers import fetch_identifier
from app.responses import ok_response, not_found_response
from app.utils import object_encode, generalize_query


@bp.get("/accounts")
def get_accounts():
    query = request.args.get('query')
    query = generalize_query(query)
    limit = request.args.get('limit')
    limit = int(limit) if limit and limit.isdigit() else None
    order_by = 'last_fetched' if request.args.get('order_by') == 'last_fetched' else None

    accounts = find_accounts(query, limit, order_by)

    return ok_response(json.dumps(accounts, default=object_encode))


@bp.get("/accounts/<bank_code>/<acc_num>")
def get_account(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return not_found_response('Bank not supported')

    account = find_account(acc_num, bank)

    if account is None:
        return not_found_response('Account not found')

    return ok_response(json.dumps(account, default=object_encode))


@bp.get("/accounts/<bank_code>/<acc_num>/transactions")
def get_transactions(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return not_found_response('Bank not supported')

    account = find_account(acc_num, bank)

    if account is None:
        return not_found_response('Account not found')

    transactions = find_transactions(acc_num, bank)

    return ok_response(json.dumps(transactions, default=object_encode))


@bp.post("/accounts/<bank_code>/<acc_num>/updates")
def fetch_transactions(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return not_found_response('Bank not supported')

    account = find_account(acc_num, bank)

    if account is None:
        return not_found_response('Account not found')

    account_request = AccountUpdate(account_number=account.number, account_bank=account.bank,
                                    status=UpdateStatus.PENDING, started=datetime.now())
    save_update(account_request)
    celery.send_task('app.tasks.fetch_transactions', args=[account_request.id])

    # Return 202 Accepted with Location of the created resource
    return app.response_class(
        status=202,
        headers={'Location': f"/accounts/{bank_code}/{acc_num}/updates/{account_request.id}"})


@bp.get("/accounts/<bank_code>/<acc_num>/updates")
def get_updates(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return not_found_response('Bank not supported')

    # TODO implement real solution

    return ok_response(json.dumps({"updates": [], "updatable": True}))


@bp.get("/accounts/<bank_code>/<acc_num>/updates/<update_id>")
def get_update(bank_code: str, acc_num: str, update_id: int):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return not_found_response('Bank not supported')

    update = find_update(update_id)

    if update is None or update.account_bank != bank or update.account_number != acc_num:
        return not_found_response('Update not found')

    return ok_response(json.dumps(update, default=str))


@bp.get("/identifiers/<identifier>")
def get_identifier(identifier: str):
    name = fetch_identifier(identifier)

    return ok_response(json.dumps({"identifier": identifier, "name": name}))


#  TODO temporary, remove in production
@bp.get("/admin/accounts/<bank_code>")
def fetch_accounts(bank_code):
    celery.send_task('app.tasks.fetch_accounts', args=[bank_code])
    return 202

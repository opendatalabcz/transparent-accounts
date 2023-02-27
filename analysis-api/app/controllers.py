import json
from datetime import datetime

from flask import request

from app import app, celery, bp, banks
from app.models import Bank, AccountUpdate, UpdateStatus
from app.queries import find_account, find_accounts, get_accounts_count
from app.queries import find_accounts_by_identifier_occurrence, find_accounts_by_counter_account_occurrence
from app.queries import find_transactions, find_update, find_updates, save_update
from app.responses import ok_response, not_found_response, bad_request_response
from app.utils import is_updatable, generalize_query, object_encode


@bp.get("/banks")
def get_banks():
    # Get banks from config and calculate the number of accounts for each bank
    for bank in banks:
        bank['accounts_count'] = get_accounts_count(Bank(bank['code']))

    # Filter out not supported banks (banks with 0 accounts)
    filtered_banks = list(filter(lambda b: b['accounts_count'] > 0, banks))
    return ok_response(json.dumps(filtered_banks))


@bp.get("/accounts")
def get_accounts():
    # Get and generalize query, so that it can be used more broadly
    query = request.args.get('query')
    query = generalize_query(query)
    # Get limit and convert it to int or None (meaning no limit)
    limit = request.args.get('limit')
    limit = int(limit) if limit and limit.isdigit() else None
    # Only allow ordering by 'last_fetched' if requested, otherwise order by 'number'
    order_by = 'last_fetched' if request.args.get('order_by') == 'last_fetched' else 'number'

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

    # Check if the account is updatable
    if not is_updatable(account):
        return bad_request_response('Account is not updatable')

    # Create a new update request, save it to the database and send a task using Celery
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

    if find_account(acc_num, bank) is None:
        return not_found_response('Account not found')

    updates = find_updates(acc_num, bank)

    return ok_response(json.dumps(updates, default=str))


@bp.get("/accounts/<bank_code>/<acc_num>/updates/<update_id>")
def get_update(bank_code: str, acc_num: str, update_id: int):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return not_found_response('Bank not supported')

    update = find_update(update_id)

    # Update not found or the update's account or bank differs from the requested one
    if update is None or update.account_bank != bank or update.account_number != acc_num:
        return not_found_response('Update not found')

    return ok_response(json.dumps(update, default=str))


@bp.get("/accounts/<bank_code>/<acc_num>/status")
def get_status(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        return not_found_response('Bank not supported')

    account = find_account(acc_num, bank)

    if account is None:
        return not_found_response('Account not found')

    # Get the last update and check if the account is updatable
    updates = find_updates(acc_num, bank)
    last_update_status = updates[0].status.name if len(updates) > 0 else None
    updatable = is_updatable(account)

    return ok_response(json.dumps({"status": last_update_status, "updatable": updatable}, default=str))


@bp.get("/occurrences")
def get_occurrences():
    identifier = request.args.get('identifier')
    counter_account = request.args.get('counter_account')

    # Exactly one of identifier or counter_account parameter must be specified
    if (identifier is None and counter_account is None) or (identifier is not None and counter_account is not None):
        return bad_request_response('Exactly one of the identifier or counter_account query parameters must be specified')

    if identifier is not None:
        occurrences = find_accounts_by_identifier_occurrence(identifier)
    elif counter_account is not None:
        occurrences = find_accounts_by_counter_account_occurrence(counter_account)

    return ok_response(json.dumps(occurrences, default=object_encode))


#  TODO temporary, remove in production
@bp.get("/admin/accounts/<bank_code>")
def fetch_accounts(bank_code):
    celery.send_task('app.tasks.fetch_accounts', args=[bank_code])
    return 202

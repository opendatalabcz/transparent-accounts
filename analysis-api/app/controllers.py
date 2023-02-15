import json
from datetime import datetime

from flask import request

from app import app, celery, bp
from app.models import Bank, AccountUpdate, UpdateStatus
from app.queries import find_accounts_count, find_account, find_transactions, find_accounts, find_update, find_updates
from app.queries import save_update, find_accounts_by_identifier_occurrence, find_accounts_by_counter_account_occurrence
from app.responses import ok_response, not_found_response, bad_request_response
from app.utils import is_updatable, generalize_query, object_encode


@bp.get("/banks")
def get_banks():
    # TODO: move to config
    banks = [
        {
            'shortcut': Bank.CSAS.name,
            'name': 'Česká spořitelna',
            'url': 'https://www.csas.cz/',
            'code': Bank.CSAS.value,
            'accounts_count': find_accounts_count(Bank.CSAS)
        },
        {
            'shortcut': Bank.CSOB.name,
            'name': 'Československá obchodní banka',
            'url': 'https://www.csob.cz/',
            'code': Bank.CSOB.value,
            'accounts_count': find_accounts_count(Bank.CSOB)
        },
        {
            'shortcut': Bank.FIO.name,
            'name': 'Fio banka',
            'url': 'https://www.fio.cz/',
            'code': Bank.FIO.value,
            'accounts_count': find_accounts_count(Bank.FIO)
        },
        {
            'shortcut': Bank.KB.name,
            'name': 'Komerční banka',
            'url': 'https://www.kb.cz/',
            'code': Bank.KB.value,
            'accounts_count': find_accounts_count(Bank.KB)
        },
        {
            'shortcut': Bank.MONETA.name,
            'name': 'Moneta Money Bank',
            'url': 'https://www.moneta.cz/',
            'code': Bank.MONETA.value,
            'accounts_count': find_accounts_count(Bank.MONETA)
        },
        {
            'shortcut': Bank.RB.name,
            'name': 'Raiffeisenbank',
            'url': 'https://www.rb.cz/',
            'code': Bank.RB.value,
            'accounts_count': find_accounts_count(Bank.RB)
        }
    ]

    # Filter out not supported banks (no accounts)
    banks = list(filter(lambda bank: bank['accounts_count'] > 0, banks))
    return ok_response(json.dumps(banks))


@bp.get("/accounts")
def get_accounts():
    query = request.args.get('query')
    query = generalize_query(query)
    limit = request.args.get('limit')
    limit = int(limit) if limit and limit.isdigit() else None
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
    updatable = is_updatable(updates)

    return ok_response(json.dumps({"updates": updates, "updatable": updatable}, default=str))


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


@bp.get("/occurrences")
def get_occurrences():
    identifier = request.args.get('identifier')
    counter_account = request.args.get('counter_account')

    # Exactly one of identifier or counter_account parameter must be specified
    if (identifier is None and counter_account is None) or (identifier is not None and counter_account is not None):
        return bad_request_response('Exactly one of the identifier or counter_account parameters must be specified')

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

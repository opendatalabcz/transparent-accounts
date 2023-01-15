import json

from flask import request

from app import app, celery, bp
from app.models import Bank
from app.queries import find_account, find_accounts
from app.utils import object_encode, generalize_query


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


@bp.get("/admin/accounts/<bank_code>")
def fetch_accounts(bank_code):
    celery.send_task('app.tasks.fetch_accounts', args=[bank_code])
    return "<h1>Success!</h1>"


@bp.get("/admin/transactions/<bank_code>/<acc_num>")
def fetch_transactions(bank_code, acc_num):
    celery.send_task('app.tasks.fetch_transactions', args=[bank_code, acc_num])
    return "<h1>Success!</h1>"

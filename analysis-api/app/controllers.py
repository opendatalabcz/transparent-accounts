import json

from app import app, celery, bp
from app.queries import find_account
from app.utils import object_encode


@bp.get("/accounts/<acc_num>")
def get_account(acc_num):
    account = find_account(acc_num)

    if account is None:
        return  # TODO

    response = app.response_class(
        response=json.dumps(account, default=object_encode),
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

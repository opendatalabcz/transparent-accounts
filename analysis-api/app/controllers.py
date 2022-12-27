import json

from app import app, celery, bp
from app.queries import find_account
from app.utils import json_encode


@bp.get("/accounts/<acc_num>")
def get_account(acc_num):
    account = find_account(acc_num)

    if account is None:
        return  # TODO

    response = app.response_class(
        response=json.dumps(account, default=json_encode),
        mimetype='application/json'
    )
    return response


@bp.get("/accounts/tmp/<bank_code>")
def fetch_accounts(bank_code):
    celery.send_task('app.tasks.fetch_accounts', args=[bank_code])
    return "<h1>Success!</h1>"


@bp.get("/transactions/tmp/<bank_code>/<acc_num>")
def fetch_transactions(bank_code, acc_num):
    celery.send_task('app.tasks.fetch_transactions', args=[bank_code, acc_num])
    return "<h1>Success!</h1>"

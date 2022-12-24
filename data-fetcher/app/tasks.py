import os
from collections import namedtuple
from datetime import date

from celery import Celery

from .queries import get_account, save_accounts, save_transactions
from .fetcher.csac import CSASAccountFetcher, CSASTransactionFetcher
from .fetcher.fio import FioAccountFetcher, FioTransactionFetcher
from .fetcher.kb import KBAccountFetcher, KBTransactionFetcher


app = Celery('data-fetcher', broker=os.getenv('CELERY_BROKER_URL'))

Fetcher = namedtuple('Fetcher', 'account transaction')

banks = {
    '0800': Fetcher(CSASAccountFetcher, CSASTransactionFetcher),
    '2010': Fetcher(FioAccountFetcher, FioTransactionFetcher),
    '0100': Fetcher(KBAccountFetcher, KBTransactionFetcher),
}


@app.task
def fetch_accounts(bank_code: str):
    if bank_code not in banks:
        return  # TODO

    fetcher = banks.get(bank_code).account()
    accounts = fetcher.fetch()
    save_accounts(accounts)


@app.task
def fetch_transactions(bank_code: str, acc_num: str):
    if bank_code not in banks:
        return  # TODO

    account = get_account(acc_num)

    if account is None:
        return  # TODO

    if account.archived:
        return  # TODO

    fetcher = banks.get(bank_code).transaction(account)
    transactions = fetcher.fetch()
    account.last_fetched = date.today()
    save_transactions(account, transactions)

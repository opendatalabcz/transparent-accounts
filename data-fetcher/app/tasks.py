import os
from collections import namedtuple

from celery import Celery

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
def test(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def add(a, b):
    return a + b


@app.task
def fetch_accounts(bank_code: str):
    if bank_code not in banks:
        return  # TODO

    fetcher = banks.get(bank_code).account()
    fetcher.fetch()


@app.task
def fetch_transactions(bank_code: str, acc_num: str):
    if bank_code not in banks:
        return  # TODO

    fetcher = banks.get(bank_code).transaction(acc_num)
    fetcher.fetch()

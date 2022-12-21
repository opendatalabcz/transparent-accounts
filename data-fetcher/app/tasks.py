from collections import namedtuple
from celery import Celery
from account_fetcher import CSASAccountFetcher, FioASAccountFetcher, KBAccountFetcher
from transaction_fetcher import CSASTransactionFetcher, FioTransactionFetcher, KBTransactionFetcher

app = Celery('data-fetcher')

Fetcher = namedtuple('Fetcher', 'account transaction')

banks = {
    '0800': Fetcher(CSASAccountFetcher, CSASTransactionFetcher),
    '2010': Fetcher(FioASAccountFetcher, FioTransactionFetcher),
    '0100': Fetcher(KBAccountFetcher, KBTransactionFetcher),
}


@app.task
def test(self):
    print('Request: {0!r}'.format(self.request))


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

import os
import logging
from collections import namedtuple
from datetime import date

from celery import Celery

from app.models import Bank
from app.queries import find_account, save_accounts, save_transactions
from app.fetcher.csac import CSASAccountFetcher, CSASTransactionFetcher
from app.fetcher.fio import FioAccountFetcher, FioTransactionFetcher
from app.fetcher.kb import KBAccountFetcher, KBTransactionFetcher

app = Celery('data-fetcher', broker=os.getenv('CELERY_BROKER_URL'))

Fetcher = namedtuple('Fetcher', 'account transaction')

banks = {
    Bank.CSAC: Fetcher(CSASAccountFetcher, CSASTransactionFetcher),
    Bank.FIO: Fetcher(FioAccountFetcher, FioTransactionFetcher),
    Bank.KB: Fetcher(KBAccountFetcher, KBTransactionFetcher),
}


@app.task
def fetch_accounts(bank_code: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        logging.warning(f"Unsupported bank: {bank_code}")
        return

    fetcher = banks[bank].account()
    accounts = fetcher.fetch()
    save_accounts(accounts, bank)


@app.task
def fetch_transactions(bank_code: str, acc_num: str):
    try:
        bank = Bank(bank_code)
    except ValueError:
        logging.warning(f"Unsupported bank: {bank_code}")
        return

    account = find_account(acc_num)

    if account is None:
        return  # TODO

    if account.archived:
        return  # TODO

    fetcher = banks[bank].transaction(account)
    transactions = fetcher.fetch()
    account.last_fetched = date.today()
    save_transactions(account, transactions)

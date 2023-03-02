import logging
import os
from collections import namedtuple
from datetime import datetime

from celery import Celery

from app.fetcher.csas import CSASAccountFetcher, CSASTransactionFetcher
from app.fetcher.fio import FioAccountFetcher, FioTransactionFetcher
from app.fetcher.kb import KBAccountFetcher, KBTransactionFetcher
from app.models import Bank, UpdateStatus
from app.queries import find_account, save_accounts, save_transactions, find_update, save_update

app = Celery('data-fetcher', broker=os.getenv('CELERY_BROKER_URL'))

Fetcher = namedtuple('Fetcher', 'account_fetcher transaction_fetcher')

banks = {
    Bank.CSAS: Fetcher(CSASAccountFetcher, CSASTransactionFetcher),
    Bank.FIO: Fetcher(FioAccountFetcher, FioTransactionFetcher),
    Bank.KB: Fetcher(KBAccountFetcher, KBTransactionFetcher),
}


@app.task
def fetch_accounts(bank_code: str):
    try:
        bank = Bank(bank_code)
        fetcher = banks[bank].account_fetcher()
    except ValueError:
        logging.warning(f"Unsupported bank: {bank_code}")
        return

    logging.info(f"Fetching of {bank} accounts for started.")

    try:
        accounts = fetcher.fetch()
        save_accounts(accounts, bank)
    except Exception:
        logging.exception(f"Fetching of {bank} accounts was interrupted.")
        return

    logging.info(f"Fetching of {bank} accounts was successful.")


@app.task
def fetch_transactions(update_id: int):
    acc_update = find_update(update_id)

    if acc_update is None:
        logging.warning(f"Account update request with id {update_id} was not found.")
        return

    account = find_account(acc_update.account_number, acc_update.account_bank)

    if account is None:
        logging.warning(f"Account {acc_update.account_number}/{acc_update.account_bank.value} not found.")
        save_update(acc_update, UpdateStatus.FAILURE)
        return

    logging.info(f"Fetching of {account.number}/{account.bank.value} transactions started.")
    fetcher = banks[account.bank].transaction_fetcher(account)

    try:
        transactions = fetcher.fetch()
        account.last_fetched = datetime.now()
        save_transactions(account, transactions)
    except Exception:
        logging.exception(f"Fetching of {account.number}/{account.bank.value} transactions was interrupted.")
        save_update(acc_update, UpdateStatus.FAILURE)
        return

    logging.info(f"Fetching of {account.number}/{account.bank.value} transactions was successful.")
    save_update(acc_update, UpdateStatus.SUCCESS)

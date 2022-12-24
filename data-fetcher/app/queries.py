from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from . import engine
from .models import Account


def get_account(acc_num: str) -> Optional[Account]:
    with Session(engine) as s:
        account = s.get(Account, acc_num)
    return account


def save_accounts(accounts: list) -> None:
    # Save current datetime
    updated = datetime.now()
    # This way of upserting is very slow, but very clear
    # Speed is not important here (can be made faster though)
    with Session(engine) as s:
        for account in accounts:
            # Mark account as just updated and not archived
            account.last_updated = updated
            account.archived = False
            s.merge(account)

        # Mark accounts that have not been updated as archived
        s.query(Account).filter(Account.last_updated != updated).update({Account.archived: True})
        s.commit()


def save_transactions(account: Account, transactions: list) -> None:
    with Session(engine) as s:
        s.add(account)
        s.add_all(transactions)
        s.commit()

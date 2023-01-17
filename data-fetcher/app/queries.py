from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app import engine
from app.models import Account, Bank, AccountUpdate, UpdateStatus


def find_account(acc_num: str, bank: Bank) -> Optional[Account]:
    """
    Finds Account by its number.
    """
    with Session(engine) as s:
        account = s.get(Account, (acc_num, bank))
    return account


def save_accounts(accounts: list, bank: Bank) -> None:
    """
    Performs the correct operation - update or insert - based on the primary key of the account.
    Then marks all non-updated or not inserted accounts as archived.
    """
    # Save current datetime
    updated = datetime.now()
    # This way of upserting is very slow, but very clear
    # Speed is not crucial here (could be made faster though)
    with Session(engine) as s:
        for account in accounts:
            # Mark account as just updated and not archived
            # Attribute archived is False by default, but it may happen that we make the archived account active again
            account.last_updated = updated
            account.archived = False
            s.merge(account)

        # Mark accounts from the same bank that have not been updated as archived
        s.query(Account).filter(Account.bank == bank, Account.last_updated != updated).update({Account.archived: True})
        s.commit()


def save_transactions(account: Account, transactions: list) -> None:
    """
    Updates the account and inserts transactions in the database.
    """
    with Session(engine) as s:
        s.add(account)
        s.add_all(transactions)
        s.commit()
        s.refresh(account)


def find_update(update_id: int) -> Optional[AccountUpdate]:
    """
    Find AccountUpdate by its ID.
    """
    with Session(engine) as s:
        request = s.get(AccountUpdate, update_id)
    return request


def save_update(account_update: AccountUpdate, status: UpdateStatus) -> None:
    """
    Updates the AccountUpdate status.
    """
    with Session(engine) as s:
        account_update.status = status
        account_update.ended = datetime.now()
        s.add(account_update)
        s.commit()

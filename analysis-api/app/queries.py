from datetime import datetime
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app import engine
from app.models import Account, Bank, AccountUpdate, UpdateStatus


def find_account(acc_num: str, bank: Bank) -> Optional[Account]:
    """
    Find Account with Transactions by its number.
    """
    with Session(engine) as s:
        # Select account with transactions, it's important to force joinedload here
        account = s.get(Account, (acc_num, bank), options=[joinedload(Account.transactions)])
    return account


def find_accounts(query: Optional[str]) -> list[Account]:
    """
    Find Accounts by the query string.
    The query string is case-insensitive compared to the number, name or owner of the account for a partial match.
    In case the query string is None, all accounts are returned.
    """
    # Query not specified - return all accounts
    if query is None:
        with Session(engine) as s:
            accounts = s.query(Account).all()
        return accounts

    # Query specified - construct the match query
    search = "%{}%".format(query)
    or_criteria = or_(Account.number.ilike(search), Account.name.ilike(search), Account.owner.ilike(search))

    with Session(engine) as s:
        accounts = s.query(Account).filter(or_criteria).all()
    return accounts


def find_update(update_id: int) -> Optional[AccountUpdate]:
    """
    Find AccountRequest by its ID.
    """
    with Session(engine) as s:
        request = s.get(AccountUpdate, update_id)
    return request


def save_update(account_update: AccountUpdate, status: UpdateStatus) -> None:
    """
    Updates the AccountRequest status.
    """
    with Session(engine) as s:
        account_update.status = status
        account_update.started = datetime.now()
        s.add(account_update)
        s.commit()
        s.refresh(account_update)

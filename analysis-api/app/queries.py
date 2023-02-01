from datetime import datetime
from typing import Optional

from sqlalchemy import select, or_, Sequence
from sqlalchemy.orm import Session

from app import engine
from app.models import Account, Transaction, Bank, AccountUpdate, UpdateStatus


def find_account(acc_num: str, bank: Bank) -> Optional[Account]:
    """
    Find Account by the number and bank.
    :param acc_num: Account number
    :param bank: Bank
    :return: Account or None
    """
    with Session(engine) as s:
        return s.get(Account, (acc_num, bank))


def find_accounts(query: Optional[str], limit: Optional[int], order_by: Optional[str]) -> Sequence['Account']:
    """
    Find Accounts by the query string.
    The query string is case-insensitive compared to the number, name or owner of the account for a partial match.
    In case the query string is None, all accounts are returned.
    The result is limited to 'limit' parameter rows and order by 'order_by' parameter.
    :param query: Query string
    :param limit: Limit the number of returned rows
    :param order_by: Order by column
    :return: Sequence of Accounts
    """
    # Query not specified - return all accounts
    if query is None:
        with Session(engine) as s:
            return s.execute(select(Account).limit(limit).order_by(order_by)).scalars().all()

    # Query specified - construct the match query
    search = f"%{query}%"
    or_criteria = or_(Account.number.ilike(search), Account.name.ilike(search), Account.owner.ilike(search))

    with Session(engine) as s:
        return s.execute(select(Account).filter(or_criteria).limit(limit).order_by(order_by)).scalars().all()


def find_transactions(acc_num: str, bank: Bank) -> Sequence['Transaction']:
    """
    Find Transactions by the account number.
    :param acc_num: Account number
    :param bank: Bank
    :return: Sequence of Transactions
    """
    with Session(engine) as s:
        return s.execute(select(Transaction).
                         filter(Transaction.account_number == acc_num, Transaction.account_bank == bank).
                         order_by(Transaction.date.desc())).scalars().all()


def find_update(update_id: int) -> Optional[AccountUpdate]:
    """
    Find AccountUpdate by its ID.
    :param update_id: AccountUpdate ID
    :return: AccountUpdate or None
    """
    with Session(engine) as s:
        request = s.get(AccountUpdate, update_id)
    return request


def save_update(account_update: AccountUpdate, status: UpdateStatus) -> None:
    """
    Updates the AccountUpdate status.
    :param account_update: AccountUpdate
    :param status: New status
    """
    with Session(engine) as s:
        account_update.status = status
        account_update.started = datetime.now()
        s.add(account_update)
        s.commit()
        s.refresh(account_update)

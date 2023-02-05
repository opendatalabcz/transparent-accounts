from typing import Optional

from sqlalchemy import select, exists, and_, or_, Sequence, desc, nulls_last
from sqlalchemy.orm import Session

from app import engine
from app.models import Account, Transaction, Bank, AccountUpdate


def find_account(acc_num: str, bank: Bank) -> Optional[Account]:
    """
    Find Account by the number and the bank.
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
            return s.execute(select(Account).limit(limit).order_by(nulls_last(desc(order_by)))).scalars().all()

    # Query specified - construct the match query
    search = f"%{query}%"
    or_criteria = or_(Account.number.ilike(search), Account.name.ilike(search), Account.owner.ilike(search))

    with Session(engine) as s:
        return s.execute(select(Account).filter(or_criteria).limit(limit).order_by(nulls_last(desc(order_by)))).scalars().all()


def find_transactions(acc_num: str, bank: Bank) -> Sequence['Transaction']:
    """
    Find Transactions by the account number sorted in descending order by the date.
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
        return s.get(AccountUpdate, update_id)


def find_updates(acc_num: str, bank: Bank) -> Sequence['AccountUpdate']:
    """
    Find AccountUpdates by the account number and bank sorted in descending order by the started date.
    :param acc_num: Account number
    :param bank: Bank
    :return: Sequence of AccountUpdates
    """
    with Session(engine) as s:
        return s.execute(select(AccountUpdate).
                         filter(AccountUpdate.account_number == acc_num, AccountUpdate.account_bank == bank).
                         order_by(AccountUpdate.started.desc())).scalars().all()


def save_update(account_update: AccountUpdate) -> None:
    """
    Save the AccountUpdate with the given status.
    :param account_update: AccountUpdate
    """
    with Session(engine) as s:
        s.add(account_update)
        s.commit()
        s.refresh(account_update)


def find_accounts_by_identifier_occurrence(identifier: str) -> Sequence['Account']:
    """
    Find accounts by the occurrence of the identifier in their transactions.
    :param identifier: counter account identifier (IČO)
    :return: Sequence of Accounts
    """
    # Construct the exists criteria - the account has at least one transaction with the given identifier
    exists_criteria = exists().where(
        and_(Transaction.account_number == Account.number, Transaction.account_bank == Account.bank,
             Transaction.ca_identifier == identifier))
    # Construct the select statement
    select_statement = select(Account).where(exists_criteria)
    with Session(engine) as s:
        return s.execute(select_statement).scalars().all()


def find_accounts_by_counter_account_occurrence(counter_account: str) -> Sequence['Account']:
    """
    Find accounts by the occurrence of the counter account in their transactions.
    :param counter_account: counter account
    :return: Sequence of Accounts
    """
    # Construct the exists criteria - the account has at least one transaction with the given counter account
    exists_criteria = exists().where(
        and_(Transaction.account_number == Account.number, Transaction.account_bank == Account.bank,
             Transaction.counter_account == counter_account))
    # Construct the select statement
    select_statement = select(Account).where(exists_criteria)
    with Session(engine) as s:
        return s.execute(select_statement).scalars().all()

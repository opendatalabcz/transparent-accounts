from typing import Optional

from sqlalchemy import select, exists, and_, or_, Sequence, ScalarResult, desc, nulls_last, func
from sqlalchemy.orm import Session

from app import engine
from app.models import Account, Transaction, Bank, AccountUpdate


def find_account(acc_num: str, bank: Bank) -> Optional[Account]:
    """
    Find Account by the number and the bank.
    """
    with Session(engine) as s:
        return s.get(Account, (acc_num, bank))


def find_accounts(query: Optional[str], limit: Optional[int], order_by: Optional[str]) -> Sequence['Account']:
    """
    Find Accounts by the query string.
    The query string is compared to the number, name or owner of the account for a partial match.
    In case the query string is None, all accounts are returned.
    The result is limited to 'limit' parameter rows and ordered by 'order_by' parameter.
    The result is ordered in such a way that null values are last.
    :param query: Query string, empty for all accounts
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
    or_criteria = or_(Account.number.like(search), Account.name_search.like(search), Account.owner_search.like(search))

    with Session(engine) as s:
        return s.execute(select(Account).filter(or_criteria).limit(limit).order_by(nulls_last(desc(order_by)))).scalars().all()


def find_accounts_by_identifier_occurrence(identifier: str) -> Sequence['Account']:
    """
    Find accounts by the occurrence of the counter account identifier (IČO) in their transactions.
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
    """
    # Construct the exists criteria - the account has at least one transaction with the given counter account
    exists_criteria = exists().where(
        and_(Transaction.account_number == Account.number, Transaction.account_bank == Account.bank,
             Transaction.counter_account == counter_account))
    # Construct the select statement
    select_statement = select(Account).where(exists_criteria)
    with Session(engine) as s:
        return s.execute(select_statement).scalars().all()


def get_accounts_count(bank: Bank) -> ScalarResult['int']:
    """
    Find the number of active (not archived) Accounts by the Bank.
    """
    with Session(engine) as s:
        return s.scalars(select(func.count()).select_from(Account).filter_by(bank=bank, archived=False)).one()


def find_transactions(acc_num: str, bank: Bank) -> Sequence['Transaction']:
    """
    Find Transactions by the account number and bank sorted in descending order by the date.
    """
    with Session(engine) as s:
        return s.execute(select(Transaction).
                         filter(Transaction.account_number == acc_num, Transaction.account_bank == bank).
                         order_by(Transaction.date.desc())).scalars().all()


def find_update(update_id: int) -> Optional[AccountUpdate]:
    """
    Find AccountUpdate by its ID.
    """
    with Session(engine) as s:
        return s.get(AccountUpdate, update_id)


def find_updates(acc_num: str, bank: Bank) -> Sequence['AccountUpdate']:
    """
    Find AccountUpdates by the account number and bank sorted in descending order by the started date.
    """
    with Session(engine) as s:
        return s.execute(select(AccountUpdate).
                         filter(AccountUpdate.account_number == acc_num, AccountUpdate.account_bank == bank).
                         order_by(AccountUpdate.started.desc())).scalars().all()


def save_update(account_update: AccountUpdate) -> None:
    """
    Save the AccountUpdate and refresh the object with the generated ID, so it can be accessed later.
    """
    with Session(engine) as s:
        s.add(account_update)
        s.commit()
        # Refresh the object, so it contains the generated ID
        s.refresh(account_update)

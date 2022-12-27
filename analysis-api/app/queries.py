from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app import engine
from app.models import Account


def find_account(acc_num: str) -> Optional[Account]:
    """
    Find Account with Transactions by the account number in the database.
    :param acc_num: fully qualified account number
    :return: optional of Account
    """
    with Session(engine) as s:
        # Select account with transactions, it's important to force joinedload here
        account = s.get(Account, acc_num, options=[joinedload(Account.transactions)])
    return account

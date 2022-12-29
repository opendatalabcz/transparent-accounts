from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app import engine
from app.models import Account


def find_account(acc_num: str) -> Optional[Account]:
    """
    Find Account with Transactions by its number.
    """
    with Session(engine) as s:
        # Select account with transactions, it's important to force joinedload here
        account = s.get(Account, acc_num, options=[joinedload(Account.transactions)])
    return account

from datetime import datetime

from sqlalchemy.orm import Session

from . import engine
from .models import Account


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

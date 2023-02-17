import re
from datetime import datetime, timedelta
from typing import Optional

from app.models import Account, Transaction, UpdateStatus
from app.queries import find_updates


def generalize_query(string: Optional[str]) -> Optional[str]:
    """
    Strip whitespace and try to find a bank code in the query and remove it.
    The aim is to generalize the query so that it can be used more broadly in a search.
    :param string: query string
    :return: generalized query string
    """
    if string is None:
        return None

    stripped = string.strip()
    return re.sub(r'/[0-9]{4}$', '', stripped)


def is_updatable(account: Account) -> bool:
    """
    Check if the account is updatable.
    Account is updatable if at least one of the following conditions is met:
    a) the account was never updated
    b) the last update was not from today
    c) the last update is pending for more than 1 hour
    d) the last update failed.
    :param account: Account
    :return: True if the account is updatable, False otherwise
    """
    updates = find_updates(account.number, account.bank)

    # Never updated
    if len(updates) == 0:
        return True

    last_update = updates[0]
    # Last update is not from today
    if last_update.started.date() != datetime.now().date():
        return True
    # Last update failed or is pending more than 1 hour - retry
    return last_update.status == UpdateStatus.FAILED or\
        (last_update.status == UpdateStatus.PENDING and last_update.started < datetime.now() - timedelta(hours=1))


def object_encode(o) -> dict | str:
    """
    Encode any object as dict or str.
    Special care is applied for Account and Transaction type, other types are encoded using str function.
    :param o: object of any type
    :return: encoded object as dict or str
    """
    match o:
        case Account():
            return {
                "number": o.number,
                "bank_code": o.bank.value,
                "name": o.name,
                "owner": o.owner,
                "balance": o.balance,
                "currency": o.currency,
                "description": o.description,
                "created": o.created,
                "last_updated": o.last_updated,
                "last_fetched": o.last_fetched,
                "archived": o.archived
            }
        case Transaction():
            return {
                "id": o.id,
                "date": o.date,
                "amount": o.amount,
                "currency": o.currency,
                "counter_account": o.counter_account,
                "type": o.type.name,
                "type_detail": o.str_type,
                "variable_symbol": o.variable_symbol,
                "constant_symbol": o.constant_symbol,
                "specific_symbol": o.specific_symbol,
                "description": o.description,
                "ca_identifier": o.ca_identifier,
                "ca_name": o.ca_name,
                "category": o.category.value if o.category is not None else None
            }
        case _:
            return str(o)

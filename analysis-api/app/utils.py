import re
from datetime import datetime, timedelta
from typing import Optional

from app.models import Account, Transaction, AccountUpdate, UpdateStatus


def generalize_query(string: Optional[str]) -> Optional[str]:
    """
    Strips whitespace and tries to find a bank code in the query and removes it.
    The aim is to generalize the query so that it can be used in a search.
    :param string: query string
    :return: generalized query string
    """
    if string is None:
        return None

    stripped = string.strip()
    return re.sub(r'/[0-9]{4}$', '', stripped)


def is_updatable(updates: list[AccountUpdate]) -> bool:
    """
    Checks if the account is updatable. It is expected that the updates are sorted by the started date in descending order.
    Account is updatable if one of the following conditions is met:
    a) the account was never updated
    b) the last update was not from today
    c) the last update is pending for more than 1 hour
    d) the last update failed.
    :param updates: list of updates sorted by the started date in descending order
    :return: True if the account is updatable, False otherwise
    """
    # Never updated
    if len(updates) == 0:
        return True

    last_update = updates[-1]
    # Last update is not from today
    if last_update.started.date() != datetime.now().date():
        return True
    # Last update failed or is pending more than 1 hour - retry
    return last_update.status == UpdateStatus.FAILED or\
        (last_update.status == UpdateStatus.PENDING and last_update.started < datetime.now() - timedelta(hours=1))


def object_encode(o) -> dict | str:
    """
    Encodes any object as dict or str.
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
                "currency": o.currency.name if o.currency is not None else None,
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
                "currency": o.currency.name if o.currency is not None else None,
                "counter_account": o.counter_account,
                "type": o.type.name,
                "type_detail": o.str_type,
                "variable_symbol": o.variable_symbol,
                "constant_symbol": o.constant_symbol,
                "specific_symbol": o.specific_symbol,
                "description": o.description,
                "identifier": o.identifier,
                "category": o.category.value if o.category is not None else None
            }
        case _:
            return str(o)

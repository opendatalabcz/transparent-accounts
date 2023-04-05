import re
from datetime import datetime, timedelta
from typing import Optional

from app.models import Account, UpdateStatus
from app.queries import find_updates


def generalize_query(string: Optional[str]) -> Optional[str]:
    """
    Strip whitespace, try to find a bank code in the query and remove it, convert lo lowercase and remove diacritics.
    The aim is to generalize the query so that it can be used more broadly in a search.
    :param string: query string
    :return: generalized query string
    """
    if string is None:
        return None

    stripped = string.strip()
    without_bank_code = re.sub(r'/[0-9]{4}$', '', stripped)
    return convert_to_searchable(without_bank_code)


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
    # Account is archived - not updatable
    if account.archived:
        return False

    updates = find_updates(account.number, account.bank)

    # Never updated
    if len(updates) == 0:
        return True

    last_update = updates[0]
    # Last update is not from today
    if last_update.started.date() != datetime.now().date():
        return True
    # Last update failed or is pending more than 1 hour - retry
    return last_update.status == UpdateStatus.FAILURE or\
        (last_update.status == UpdateStatus.PENDING and last_update.started < datetime.now() - timedelta(hours=1))


def convert_to_searchable(value: Optional[str]) -> Optional[str]:
    """
    Convert string to lowercase and remove diacritics.
    """
    if value is None:
        return None

    value = value.casefold()

    chars_from = ['á', 'č', 'ď', 'é', 'ě', 'í', 'ň', 'ó', 'ř', 'š', 'ť', 'ú', 'ů', 'ý', 'ž']
    chars_to = ['a', 'c', 'd', 'e', 'e', 'i', 'n', 'o', 'r', 's', 't', 'u', 'u', 'y', 'z']

    for char_from, char_to in zip(chars_from, chars_to):
        value = value.replace(char_from, char_to)

    return value

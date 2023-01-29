import re
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Optional

from app.models import Account, Transaction, TransactionType, TransactionCategory


class TransactionFetcher(ABC):

    def __init__(self, account: Account):
        self.account = account

    @abstractmethod
    def fetch(self) -> list[Transaction]:
        pass

    def get_date_from(self) -> date:
        """
        Returns the date from which the transactions should be fetched.
        The date is either the date of the last fetch
        or 2000-01-01 if the account's transactions have never been fetched before.
        :return: the date from which the transactions should be fetched
        """
        if self.account.last_fetched is None:
            return date(2000, 1, 1)
        return self.account.last_fetched

    @staticmethod
    def get_date_to() -> date:
        """
        Returns the date to which the transactions should be fetched. The date is always yesterday.
        :return: the date to which the transactions should be fetched
        """
        return date.today() - timedelta(1)

    def check_date_interval(self, transaction: Transaction) -> bool:
        return self.get_date_from() <= transaction.date <= self.get_date_to()

    @staticmethod
    def parse_identifier(string: str) -> Optional[str]:
        """
        Parses the personal identification number (IČO) from the string.
        Identifier is an 8-digit number.
        :param string:
        :return: the parsed identifier or None if the identifier was not found
        """
        # Pattern is saying that we are looking for an exactly 8-digit sequence
        # Preceded by start of string, whitespace or colon and followed by end of string, whitespace or comma
        # Example: "IČO: 12345678" or "IČO:12345678" or "12345678 ..."
        pattern = r'(?:^|\s|:)([0-9]{8})(?:$|\s|,)'
        search = re.search(pattern, string)
        return search.group(1) if search is not None else None

    @staticmethod
    def determine_category(money_amount: float, transaction_type: TransactionType) -> Optional[TransactionCategory]:
        """
        Determines the category of the transaction based on the amount and type.
        :param money_amount:
        :param transaction_type:
        :return: category if determined, None otherwise
        """
        # Incoming transaction with a very small amount is considered as a message (probably hateful) for the receiver
        # Should not be lesser than 0 but just in case
        if 1 >= money_amount > 0 and transaction_type == TransactionType.INCOMING:
            return TransactionCategory.MESSAGE
        return None

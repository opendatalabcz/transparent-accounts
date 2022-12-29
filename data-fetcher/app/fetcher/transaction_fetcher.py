from datetime import date, timedelta
from abc import ABC, abstractmethod

from app.models import Account, Transaction


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
        Returns the date to which the transactions should be fetched.
        The date is always yesterday.
        :return: the date to which the transactions should be fetched
        """
        return date.today() - timedelta(1)

    def check_date_interval(self, transaction: Transaction) -> bool:
        return self.get_date_from() <= transaction.date <= self.get_date_to()

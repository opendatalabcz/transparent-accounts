from datetime import date, timedelta
from abc import ABC, abstractmethod

from ..models import Account


class TransactionFetcher(ABC):

    def __init__(self, account: Account):
        self.account = account

    @abstractmethod
    def fetch(self) -> None:
        """
        - podivat se u uctu na "last_fetched", to je datum, kdy byly transakce naposled stazeny
        - stahnout transakce ode dne "last_fetched" + 1 do dne "today" - 1
        :return:
        """
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

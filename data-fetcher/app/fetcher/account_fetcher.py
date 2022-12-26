from abc import ABC, abstractmethod

from ..models import Account


class AccountFetcher(ABC):

    @abstractmethod
    def fetch(self) -> list[Account]:
        pass

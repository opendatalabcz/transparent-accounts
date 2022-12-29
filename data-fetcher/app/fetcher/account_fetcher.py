from abc import ABC, abstractmethod

from app.models import Account


class AccountFetcher(ABC):

    @abstractmethod
    def fetch(self) -> list[Account]:
        pass

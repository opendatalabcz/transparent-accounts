from abc import ABC, abstractmethod


class AccountFetcher(ABC):

    @abstractmethod
    def fetch(self) -> None:
        """
        - projet vsechny ucty
        - existujici (cislo uctu) update
        - nove insert
        - vsem nalezenym nastavit "last_updated" na "today"
        - ucty, ktere nebyly nalezeny oznacit jako "archived"
        """
        pass

from app.fetcher.account_fetcher import AccountFetcher
from app.models import Account


class CSOBAccountFetcher(AccountFetcher):
    def fetch(self) -> list[Account]:
        pass

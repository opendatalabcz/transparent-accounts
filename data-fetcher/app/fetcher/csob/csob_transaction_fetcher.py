from app.fetcher.transaction_fetcher import TransactionFetcher
from app.models import Transaction


class CSOBTransactionFetcher(TransactionFetcher):
    def fetch(self) -> list[Transaction]:
        pass

from datetime import date

import pytest
from flexmock import flexmock

from app.models import Account, Transaction
from app.fetcher.kb import KBTransactionFetcher


@pytest.fixture
def fetcher():
    flexmock(KBTransactionFetcher)
    KBTransactionFetcher.should_receive("get_date_from").and_return(date(2021, 1, 1))
    KBTransactionFetcher.should_receive("get_date_to").and_return(date(2021, 2, 1))

    fetcher = KBTransactionFetcher(Account(number='123456-1234567890'))
    return fetcher


def test_check_date_interval_true(fetcher):
    assert fetcher.check_date_interval(Transaction(date=date(2021, 1, 1)))
    assert fetcher.check_date_interval(Transaction(date=date(2021, 1, 15)))
    assert fetcher.check_date_interval(Transaction(date=date(2021, 2, 1)))


def test_check_date_interval_false(fetcher):
    assert not fetcher.check_date_interval(Transaction(date=date(2022, 12, 31)))
    assert not fetcher.check_date_interval(Transaction(date=date(2021, 4, 1)))
    assert not fetcher.check_date_interval(Transaction(date=date(2021, 2, 2)))
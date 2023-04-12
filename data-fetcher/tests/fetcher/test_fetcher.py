from datetime import date

import pytest
from flexmock import flexmock

from app.fetcher.transaction_fetcher import TransactionFetcher
from app.fetcher.kb import KBTransactionFetcher
from app.models import Account, Transaction


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


def test_parse_identifier():
    assert TransactionFetcher.parse_identifier('IČ: 12345678') == '12345678'
    assert TransactionFetcher.parse_identifier('IČO: 12345678') == '12345678'
    assert TransactionFetcher.parse_identifier('IČO:12345678MARKETING') == '12345678'
    assert TransactionFetcher.parse_identifier('IČO12345678') == '12345678'
    assert TransactionFetcher.parse_identifier('IČO:12345678, Marketing') == '12345678'
    assert TransactionFetcher.parse_identifier('IČO: 00000000 Marketing') == '00000000'
    assert TransactionFetcher.parse_identifier('Marketing, IČO:00000000') == '00000000'


def test_parse_identifier_none():
    assert TransactionFetcher.parse_identifier('12345678') is None
    assert TransactionFetcher.parse_identifier('IČO: 123456789') is None
    assert TransactionFetcher.parse_identifier('Faktura: 12345678') is None

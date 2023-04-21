from datetime import date

import pytest
from flexmock import flexmock

from app.fetcher.transaction_fetcher import TransactionFetcher
from app.fetcher.kb import KBTransactionFetcher
from app.models import Account, Transaction, TransactionType


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


def test_search():
    pattern = r'hello'
    string_with_pattern = 'Héllo world!'
    string_without_pattern = 'Goodbye world!'

    assert TransactionFetcher.search(pattern, string_with_pattern) is True
    assert TransactionFetcher.search(pattern, string_without_pattern) is False


def test_determine_category() -> None:
    transaction = Transaction(type=TransactionType.INCOMING, amount=0.01, description='Some description')
    assert TransactionFetcher.determine_category(transaction) == 'Vzkaz'

    transaction = Transaction(type=TransactionType.OUTGOING, description='Nákup: GOOGLE *ADS5433864005, g.co/HelpPay#, IE, dne 31.3.2023, částka 363087.18 CZK')
    assert TransactionFetcher.determine_category(transaction) == 'Google'

    transaction = Transaction(type=TransactionType.OUTGOING, description='Nákup: FACEBK *CYQENK3R32, fb.me/ads, IE, dne 1.2.2023, částka 21863.37 CZK')
    assert TransactionFetcher.determine_category(transaction) == 'Facebook'

    transaction = Transaction(type=TransactionType.OUTGOING, description='IČ: 12345678, plakáty')
    assert TransactionFetcher.determine_category(transaction) == 'Marketing'

    transaction = Transaction(type=TransactionType.OUTGOING, description='IČ: 12345678, pronajem prostor')
    assert TransactionFetcher.determine_category(transaction) == 'Pronájem'

    transaction = Transaction(type=TransactionType.OUTGOING, description='IČ: 12345678, socialni síte')
    assert TransactionFetcher.determine_category(transaction) == 'Sociální sítě'

    transaction = Transaction(type=TransactionType.OUTGOING, description='Koordinace sběru podpisů')
    assert TransactionFetcher.determine_category(transaction) == 'Sběr podpisů'

    transaction = Transaction(type=TransactionType.OUTGOING, description='Na poznámku kašlu')
    assert TransactionFetcher.determine_category(transaction) is None

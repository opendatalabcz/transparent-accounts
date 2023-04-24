from datetime import date

from app.fetcher.kb import KBAccountFetcher, KBTransactionFetcher
from app.models import Account, TransactionType


def test_parse_account_details():
    assert KBAccountFetcher.parse_details('majitel účtu: \"Hnutí Praha - Kunratice\", \r\n                                   číslo účtu: 115-5000730217/0100, \r\n                                   měna: CZK') == ('\"Hnutí Praha - Kunratice\"', '115-5000730217', 'CZK')
    assert KBAccountFetcher.parse_details('majitel účtu: Habžanský Jiří, \r\n                                   číslo účtu: 115-9594910247/0100, \r\n                                   měna: CZK') == ('Habžanský Jiří', '115-9594910247', 'CZK')
    assert KBAccountFetcher.parse_details('majitel účtu: BOJIŠTĚ s.r.o., \r\n                                   číslo účtu: 115-7210610247/0100, \r\n                                   měna: CZK') == ('BOJIŠTĚ s.r.o.', '115-7210610247', 'CZK')


def test_parse_date():
    assert KBTransactionFetcher.parse_date({'date': '17. 3.', 'year': ''}) == date(2023, 3, 17)
    assert KBTransactionFetcher.parse_date({'date': '1. 1.', 'year': '2022'}) == date(2022, 1, 1)
    assert KBTransactionFetcher.parse_date({'date': '31. 12.', 'year': '2021'}) == date(2021, 12, 31)


def test_parse_money_amount():
    assert KBTransactionFetcher.parse_money_amount('100,00 CZK') == (100, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('-6,00 CZK') == (-6, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('4 186,33 EUR') == (4186.33, 'EUR')
    assert KBTransactionFetcher.parse_money_amount('-1 100,00 EUR') == (-1100, 'EUR')
    assert KBTransactionFetcher.parse_money_amount('-2,47 EUR') == (-2.47, 'EUR')
    assert KBTransactionFetcher.parse_money_amount('0,01 CZK') == (0.01, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('1 567 601,25 CZK') == (1567601.25, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('-1 567 601,25 CZK') == (-1567601.25, 'CZK')


def test_parse_symbols():
    assert KBTransactionFetcher.parse_symbols('VS: 1, KS: 2, SS: 3') == ('1', '2', '3')
    assert KBTransactionFetcher.parse_symbols('SS: 1, VS: 2, KS: 3') == ('2', '3', '1')
    assert KBTransactionFetcher.parse_symbols('VS: 111, KS: 222') == ('111', '222', '')
    assert KBTransactionFetcher.parse_symbols('VS: 123456780') == ('123456780', '', '')
    assert KBTransactionFetcher.parse_symbols('KS: 123456780') == ('', '123456780', '')
    assert KBTransactionFetcher.parse_symbols('SS: 123456780') == ('', '', '123456780')


def test_parse_details():
    assert KBTransactionFetcher.parse_details({'info': {'title': 'Odchozí platba', 'transparentAccountInfo': ''}, 'amount': {'type': 'expense'}}) == (None, 'Odchozí platba', '')
    assert KBTransactionFetcher.parse_details({'info': {'title': 'Jakub Janeček', 'transparentAccountInfo': 'Poznámka'}, 'amount': {'type': 'income'}}) == ('Jakub Janeček', 'Příchozí platba', 'Poznámka')

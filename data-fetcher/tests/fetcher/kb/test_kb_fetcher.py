from datetime import date

from app.fetcher.kb import KBTransactionFetcher
from app.models import Account, TransactionType


def test_parse_money_amount():
    assert KBTransactionFetcher.parse_money_amount('100,00 CZK') == (100, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('-6,00 CZK') == (-6, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('4 186,33 EUR') == (4186.33, 'EUR')
    assert KBTransactionFetcher.parse_money_amount('-1 100,00 EUR') == (-1100, 'EUR')
    assert KBTransactionFetcher.parse_money_amount('-2,47 EUR') == (-2.47, 'EUR')
    assert KBTransactionFetcher.parse_money_amount('0,01 CZK') == (0.01, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('1 567 601,25 CZK') == (1567601.25, 'CZK')
    assert KBTransactionFetcher.parse_money_amount('-1 567 601,25 CZK') == (-1567601.25, 'CZK')


def test_parse_date():
    assert KBTransactionFetcher.parse_date('01.&nbsp;01.&nbsp;2022') == date(2022, 1, 1)


def test_parse_details():
    assert KBTransactionFetcher.parse_details('1<br />2<br />3', TransactionType.INCOMING) == ('1', '2', '3')
    assert KBTransactionFetcher.parse_details('1<br />2', TransactionType.INCOMING) == ('1', '2', '')
    assert KBTransactionFetcher.parse_details('1<br />2', TransactionType.OUTGOING) == (None, '1', '2')
    assert KBTransactionFetcher.parse_details('1', TransactionType.OUTGOING) == (None, '1', '')


def test_kb_transaction_to_class_incoming():
    raw = {
            "id": "361-24122022 1086 086143 100448",
            "date": "24.&nbsp;11.&nbsp;2022",
            "amount": "0,01 EUR",
            "symbols": "1 / 2 / 3",
            "notes": "Testovací uživatel<br />Příchozí platba<br />Testovací popis"
        }

    account = Account(number='000000-0123456789')
    fetcher = KBTransactionFetcher(account)

    t = fetcher.transaction_to_class(raw)

    assert t.date == date(2022, 11, 24)
    assert t.amount == 0.01
    assert t.counter_account == 'Testovací uživatel'
    assert t.type == TransactionType.INCOMING
    assert t.str_type == 'Příchozí platba'
    assert t.variable_symbol == '1'
    assert t.constant_symbol == '2'
    assert t.specific_symbol == '3'
    assert t.description == 'Testovací popis'
    assert t.account_number == '000000-0123456789'


def test_kb_transaction_to_class_outgoing():
    raw = {
            "id": "361-24122022 1086 086143 100448",
            "date": "24.&nbsp;11.&nbsp;2022",
            "amount": "-10 000,00 CZK",
            "symbols": "0 / 0 / 12345",
            "notes": "Odchozí platba<br />Testovací popis"
        }

    account = Account(number='000000-0123456789')
    fetcher = KBTransactionFetcher(account)

    t = fetcher.transaction_to_class(raw)

    assert t.date == date(2022, 11, 24)
    assert t.amount == -10000
    assert t.counter_account is None
    assert t.type == TransactionType.OUTGOING
    assert t.str_type == 'Odchozí platba'
    assert t.variable_symbol == '0'
    assert t.constant_symbol == '0'
    assert t.specific_symbol == '12345'
    assert t.description == 'Testovací popis'
    assert t.account_number == '000000-0123456789'

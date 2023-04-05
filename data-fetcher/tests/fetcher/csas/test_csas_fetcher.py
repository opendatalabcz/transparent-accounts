from datetime import date

from app.fetcher.csas.csas_account_fetcher import CSASAccountFetcher
from app.fetcher.csas.csas_transaction_fetcher import CSASTransactionFetcher
from app.models import Account, TransactionType, Bank


def test_csas_account_to_class():
    raw = {
        'accountNumber': '000000-0123456789',
        'bankCode': '0800',
        'transparencyFrom': '2015-04-10T00:00:00',
        'transparencyTo': '3000-01-01T00:00:00',
        'publicationTo': '3000-01-01T00:00:00',
        'actualizationDate': '2022-12-22T15:00:00',
        'balance': 1200.85,
        'currency': 'CZK',
        'name': 'Testovací účet',
        'iban': 'CZ19 0800 0000 0039 3617 3359'
    }

    acc = CSASAccountFetcher.account_to_class(raw)

    assert acc.number == '000000-0123456789'
    assert acc.bank == Bank.CSAS
    assert acc.name == 'Testovací účet'
    assert acc.owner == 'Testovací účet'
    assert acc.balance == 1200.85
    assert acc.currency == 'CZK'
    assert acc.description is None
    assert acc.created == date(2015, 4, 10)
    assert acc.last_updated is None
    assert acc.last_fetched is None
    assert acc.archived is None
    assert acc.inserted is None
    assert not acc.transactions


def test_csas_transaction_to_class():
    raw = {
        "amount": {
            "value": -10000.0,
            "precision": 0,
            "currency": "CZK"
        },
        "type": "80155",
        "dueDate": "2022-11-24T00:00:00",
        "processingDate": "2022-11-24T00:00:00",
        "sender": {
            "constantSymbol": "0",
            "specificSymbol": "12345",
            "name": "000000-9876543210/3030",
            "description": "Testovací popis"
        },
        "receiver": {
            "accountNumber": "000000-0123456789",
            "bankCode": "0800",
            "iban": "CZ18 0800 0000 0001 2345 6789"
        },
        "typeDescription": "Tuzemská odchozí úhrada"
    }

    account = Account(number='000000-0123456789')
    fetcher = CSASTransactionFetcher(account)

    t = fetcher.transaction_to_class(raw)

    assert t.date == date(2022, 11, 24)
    assert t.amount == -10000
    assert t.counter_account == '000000-9876543210/3030'
    assert t.type == TransactionType.OUTGOING
    assert t.type_str == 'Tuzemská odchozí úhrada'
    assert t.variable_symbol == ''
    assert t.constant_symbol == '0'
    assert t.specific_symbol == '12345'
    assert t.description == 'Testovací popis'
    assert t.account_number == '000000-0123456789'

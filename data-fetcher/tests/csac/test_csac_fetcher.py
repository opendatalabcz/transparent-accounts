from datetime import date

from app.models import Currency
from app.fetcher.csac.csas_account_fetcher import CSASAccountFetcher


def test_csac_account_map():
    raw = {
        'accountNumber': '000000-3936173359',
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

    assert acc.id is None
    assert acc.number == '000000-3936173359'
    assert acc.bank_code == '0800'
    assert acc.name == 'Testovací účet'
    assert acc.owner == 'Testovací účet'
    assert acc.balance == 1200.85
    assert acc.currency == Currency.CZK
    assert acc.description is None
    assert acc.created == date(2015, 4, 10)
    assert acc.last_updated is None
    assert acc.last_fetched is None
    assert acc.archived is None
    assert acc.inserted is None
    assert not acc.transactions

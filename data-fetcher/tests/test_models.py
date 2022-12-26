import pytest

from app.models import Currency, TransactionType


def test_currency():
    assert Currency.from_str('CZK') == Currency.CZK
    assert Currency.from_str('eur') == Currency.EUR
    assert Currency.from_str('Usd') == Currency.USD
    assert Currency.from_str('gBp') == Currency.GBP
    with pytest.raises(NotImplementedError, match='CAD'):
        Currency.from_str('CAD')


def test_transaction_type():
    assert TransactionType.from_float(-1) == TransactionType.OUTGOING
    assert TransactionType.from_float(0) == TransactionType.OUTGOING
    assert TransactionType.from_float(1) == TransactionType.INCOMING

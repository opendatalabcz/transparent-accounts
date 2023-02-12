import pytest

from app.models import TransactionType


def test_transaction_type():
    assert TransactionType.from_float(-1) == TransactionType.OUTGOING
    assert TransactionType.from_float(0) == TransactionType.OUTGOING
    assert TransactionType.from_float(1) == TransactionType.INCOMING

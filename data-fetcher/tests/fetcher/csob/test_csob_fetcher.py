from typing import Optional

import pytest

from app.fetcher.csob import CSOBTransactionFetcher


@pytest.mark.parametrize('symbols, expected', [
    (
        {
            'variableSymbol': '123',
            'constantSymbol': '456',
            'specificSymbol': '789'
        },
        ('123', '456', '789')
    ),
    (
        {
            'variableSymbol': '123',
            'constantSymbol': None,
            'specificSymbol': '456'
        },
        ('123', '', '456')
    ),
    (
        {
            'variableSymbol': None,
            'constantSymbol': None,
            'specificSymbol': None
        },
        ('', '', '')
    ),
    (
        None,
        ('', '', '')
    ),
])
def test_parse_symbols(symbols: Optional[dict], expected: tuple[str, str, str]):
    assert CSOBTransactionFetcher.parse_symbols(symbols) == expected


@pytest.mark.parametrize('transaction_detail, key, expected', [
    (
        {'message1': 'Hello ', 'message2': 'World', 'message3': None, 'message4': None},
        'message',
        'Hello World'
    ),
    (
        {'remittanceInformation1': 'This ', 'remittanceInformation2': 'is ', 'remittanceInformation3': 'a ', 'remittanceInformation4': 'test'},
        'remittanceInformation',
        'This is a test'
    ),
    (
        {'narrative1': 'Testing', 'narrative2': '123', 'narrative3': None, 'narrative4': None},
        'narrative',
        'Testing123'
    )
])
def test_parse_description(transaction_detail: dict, key: str, expected: str):
    assert CSOBTransactionFetcher.parse_description(transaction_detail, key) == expected

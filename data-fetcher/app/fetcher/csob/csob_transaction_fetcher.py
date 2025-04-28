from datetime import datetime
from typing import Optional

import requests

from app.fetcher.csob.utils import headers, get_csob_formatted_acc_num
from app.fetcher.transaction_fetcher import TransactionFetcher
from app.models import Transaction, TransactionType, TransactionTypeDetail


class CSOBTransactionFetcher(TransactionFetcher):

    API_URL = 'https://www.csob.cz/spa/finance/lta/detail/transactionList'
    ROWS_PER_PAGE = 1500

    def fetch(self) -> list[Transaction]:
        with requests.Session() as s:
            # Set mandatory headers
            s.headers.update(headers)
            body = {
                'accountList': [
                    {
                        'accountNumberM24': get_csob_formatted_acc_num(self.account.number)
                    }
                ],
                'filterList': [
                    {
                        'name': 'AccountingDate',
                        'operator': 'ge',
                        'valueList': [self.get_date_from().strftime('%Y-%m-%d')]
                    },
                    {
                        'name': 'AccountingDate',
                        'operator': 'le',
                        'valueList': [self.get_date_to().strftime('%Y-%m-%d')]
                    }
                ],
                'sortList': [
                    {
                        'name': 'AccountingDate',
                        'direction': 'ASC',
                        'order': 1
                    }
                ],
                'paging': {
                    'rowsPerPage': self.ROWS_PER_PAGE,
                    'pageNumber': 1
                }
            }
            # Initial request for transactions and also total page count
            response_data = s.post(self.API_URL, json=body).json()
            page_count = response_data['paging']['pageCount']
            transactions = response_data['accountedTransaction'] or []
            # Iterate through all pages
            for i in range(2, page_count + 1):
                body['paging']['pageNumber'] = i
                response_data = s.post(self.API_URL, json=body).json()
                transactions += response_data['accountedTransaction']
            return [self.transaction_to_class(t) for t in transactions]

    def transaction_to_class(self, t: dict) -> Transaction:
        amount = t['baseInfo']['accountAmountData']['amount']
        transaction_data = self.parse_transaction(t)
        # Parse the counter account identifier and name
        ca_identifier = self.parse_identifier(transaction_data.get('description', ''))
        ca_name = self.fetch_identifier_name(ca_identifier) if ca_identifier else None

        transaction = Transaction(
            # Timestamp in milliseconds provided
            date=datetime.fromtimestamp(t['baseInfo']['accountingDate'] / 1000).date(),
            amount=amount,
            currency=t['baseInfo']['accountAmountData']['currencyCode'],
            counter_account=transaction_data.get('counter_account'),
            type=TransactionType.from_float(amount),
            type_str=t['baseInfo']['transactionDescription'],
            variable_symbol=transaction_data.get('variable_s', ''),
            constant_symbol=transaction_data.get('constant_s', ''),
            specific_symbol=transaction_data.get('specific_s', ''),
            description=transaction_data.get('description', ''),
            ca_identifier=ca_identifier,
            ca_name=ca_name,
            account_number=self.account.number,
            account_bank=self.account.bank
        )
        transaction.type_detail = self.determine_detail_type_override(transaction, t['transactionTypeChoice'])
        transaction.category = self.determine_category(transaction)
        return transaction

    def parse_transaction(self, t: dict) -> dict:
        transaction_type_choice = t.get('transactionTypeChoice')
        if not transaction_type_choice:
            return {}

        switch = {
            'domesticPayment': self.process_domesticPayment,
            'crossborderPayment': self.process_crossborderPayment,
            'sepaCreditTransfer': self.process_sepaCreditTransfer,
            'tbca': self.process_domesticPayment,
            'otherTransaction': self.process_otherTransaction
        }
        transaction_type = next((k for k, v in t['transactionTypeChoice'].items() if v is not None), None)
        if transaction_type in switch:
            return switch[transaction_type](t['transactionTypeChoice'][transaction_type])
        return {}

    @staticmethod
    def parse_symbols(symbols: Optional[dict]) -> tuple[str, str, str]:
        if symbols is None:
            return '', '', ''
        # Retrieve transactions symbols if not null
        variable_s = symbols['variableSymbol'] or ''
        constant_s = symbols['constantSymbol'] or ''
        specific_s = symbols['specificSymbol'] or ''
        return variable_s, constant_s, specific_s

    @staticmethod
    def parse_description(descriptions: Optional[dict], key: str) -> str:
        if descriptions is None:
            return ''

        parsed_descriptions = [descriptions[f"{key}{i}"] for i in range(1, 5)]
        return ''.join(s if s is not None else '' for s in parsed_descriptions)

    def process_domesticPayment(self, transaction_data: dict) -> dict:
        counter_account = transaction_data['partyName']
        description = self.parse_description(transaction_data['message'], 'message')
        variable_s, constant_s, specific_s = self.parse_symbols(transaction_data['symbols'])
        return {
            'counter_account': counter_account, 'description': description,
            'variable_s': variable_s, 'constant_s': constant_s, 'specific_s': specific_s,
        }

    def process_crossborderPayment(self, transaction_data: dict) -> dict:
        counter_account = (transaction_data['partyAddress'] or {}).get('addressLine1')
        description = self.parse_description(transaction_data['remittanceInformation'], 'remittanceInformation')
        return {'counter_account': counter_account, 'description': description}

    def process_sepaCreditTransfer(self, transaction_data: dict) -> dict:
        counter_account = transaction_data['partyName']
        return {'counter_account': counter_account}

    def process_otherTransaction(self, transaction_data: dict) -> dict:
        counter_account = transaction_data['partyName']
        description = self.parse_description(transaction_data['narrative'], 'narrative')
        variable_s, constant_s, specific_s = self.parse_symbols(transaction_data['symbols'])
        return {
            'counter_account': counter_account, 'description': description,
            'variable_s': variable_s, 'constant_s': constant_s, 'specific_s': specific_s,
        }

    @staticmethod
    def determine_detail_type_override(transaction: Transaction, transaction_detail: dict) -> Optional[TransactionTypeDetail]:
        """
        Determine the detail type of the transaction.
        :param transaction: Transaction to determine the detail type for
        :param transaction_detail: Transaction detail dictionary
        :return: detail type if determined, None otherwise
        """
        # Fee
        if (transaction_detail or {}).get('fee') is not None:
            return TransactionTypeDetail.FEE
        # Try default detail type determination
        return TransactionFetcher.determine_detail_type(transaction)

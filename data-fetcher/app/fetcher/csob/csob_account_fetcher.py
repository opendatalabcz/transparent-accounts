from datetime import datetime

import requests

from app.fetcher.csob.utils import headers
from app.fetcher.account_fetcher import AccountFetcher
from app.models import Account, Bank
from app.utils import get_fully_qualified_acc_num


class CSOBAccountFetcher(AccountFetcher):

    API_URL = 'https://www.csob.cz/spa/finance/lta/overview/accountList'

    def fetch(self) -> list[Account]:
        with requests.Session() as s:
            # Set mandatory headers
            s.headers.update(headers)
            # First request to get the number of records
            body = {'displayParams': {'pagingRequest': {'rowsPerPage': 1, 'pageNumber': 1}}}
            response_data = s.post(self.API_URL, json=body).json()
            record_count = response_data['pagingResponse']['recordCount']
            # Second request to get all records
            body['displayParams']['pagingRequest']['rowsPerPage'] = record_count
            response_data = s.post(self.API_URL, json=body).json()

            return list(map(self.account_to_class, response_data['accountList']))

    @staticmethod
    def account_to_class(acc: dict) -> Account:
        return Account(number=get_fully_qualified_acc_num(acc['accountPoIdentificationDisplay']['displayNumber']),
                       bank=Bank.CSOB,
                       name=acc['accountName'],
                       owner=acc['accountName'],
                       balance=acc['balance']['actualBalance'],
                       currency=acc['accountPoIdentificationDisplay']['currencyCode'],
                       # Timestamp in milliseconds provided
                       created=datetime.fromtimestamp(acc['transparentAccountDetail']['periodFrom'] / 1000).date())


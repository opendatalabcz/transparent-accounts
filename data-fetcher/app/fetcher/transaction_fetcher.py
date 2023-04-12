import re
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Optional
from xml.etree import ElementTree

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.models import Account, Transaction, TransactionType, TransactionTypeDetail
from app.utils import convert_to_searchable


class TransactionFetcher(ABC):

    def __init__(self, account: Account):
        self.account = account

    @abstractmethod
    def fetch(self) -> list[Transaction]:
        pass

    def get_date_from(self) -> date:
        """
        Return the date from which the transactions should be fetched.
        The date is either the date of the last fetch
        or 2015-01-01 if the account's transactions have never been fetched before.
        :return: the date from which the transactions should be fetched
        """
        if self.account.last_fetched is None:
            return date(2015, 1, 1)
        return self.account.last_fetched.date()

    def get_date_to(self) -> date:
        """
        Return the date to which the transactions should be fetched. The date is ALWAYS yesterday.
        :return: the date to which the transactions should be fetched
        """
        return date.today() - timedelta(1)

    def check_date_interval(self, transaction: Transaction) -> bool:
        """
        Check if the transaction's date is within the fetching date_from and date_to interval.
        """
        return self.get_date_from() <= transaction.date <= self.get_date_to()

    @staticmethod
    def parse_identifier(string: str) -> Optional[str]:
        """
        Parse the personal identification number (IČO) from the string.
        Identifier is an 8-digit number. Identifier is parsed only if the string contains the word 'IČ'.
        :param string:
        :return: the parsed identifier or None if the identifier was not found
        """
        # Pattern is saying that we are looking for an exactly 8-digit sequence (not longer, not shorter)
        pattern = r'((?<![0-9])[0-9]{8}(?![0-9]))'
        search = re.search(pattern, string)
        # Identifier found and string contains the word IČ
        return search.group(1) if search is not None and 'IČ' in string else None

    @staticmethod
    def fetch_identifier_name(identifier: str) -> Optional[str]:
        """
        Fetch the name of the company with the given identifier from the ARES database.
        :param identifier: identifier of the company (IČO)
        :return: name of the company or None if not found
        """
        # Retry the request 3 times with exponential backoff
        s = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('https://', adapter)
        # Fetch the XML response from the ARES database
        response = s.get(f"https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico={identifier}")
        tree = ElementTree.fromstring(response.content)
        # Namespace of the ARES XML schema
        ns = {'are': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1'}
        # Use XML path's './/' to search for the element in the whole tree
        element = tree.find('.//are:Obchodni_firma', ns)
        return element.text if element is not None else None

    @staticmethod
    def determine_detail_type(transaction: Transaction) -> TransactionTypeDetail:
        """
        Determine the detail type of the transaction.
        It is expected that every transaction fetcher has its own implementation of this method
        and this concrete implementation is called as a fallback when the fetcher does not determine the detail type.
        :param transaction: Transaction to determine the detail type for
        :return: detail type if determined, None otherwise
        """
        # Only resolve INCOMING x OUTGOING transactions
        return TransactionTypeDetail.INCOMING if transaction.type == TransactionType.INCOMING else TransactionTypeDetail.OUTGOING

    @staticmethod
    def determine_category(transaction: Transaction) -> Optional[str]:
        """
        Determine the category of the transaction.
        :param transaction: Transaction to determine the category for
        :return: category if determined, None otherwise
        """
        # Incoming transaction with a very small amount is considered as a message (probably hateful) for the receiver
        if transaction.type == TransactionType.INCOMING and 1 >= transaction.amount > 0:
            return 'Vzkaz'
        # No more categories to determine for incoming transactions
        if transaction.type == TransactionType.INCOMING:
            return None
        if TransactionFetcher.search(r'google', transaction.description):
            return 'Google'
        if TransactionFetcher.search(r'fb.me/ads', transaction.description):
            return 'Facebook'
        if TransactionFetcher.search(r'marketing|plakat|letak|billboard|banner|samolepky|vylep|tisk|propagac', transaction.description):
            return 'Marketing'
        if TransactionFetcher.search(r'pronajem', transaction.description):
            return 'Pronájem    '
        if TransactionFetcher.search(r'socialni síte|socialnich siti|soc. siti|socialni media', transaction.description):
            return 'Sociální sítě'
        if TransactionFetcher.search(r'podpis', transaction.description):
            return 'Sběr podpisů'
        return None

    @staticmethod
    def search(pattern: str, string: str) -> bool:
        """
        Search for the pattern in the searchable version of the string.
        Searchable version of the string is the string converted to lowercase and with diacritics removed.
        :param pattern: pattern to search for
        :param string: string to search in
        :return: True if the pattern was found, False otherwise
        """
        string = convert_to_searchable(string)
        return re.search(pattern, string) is not None

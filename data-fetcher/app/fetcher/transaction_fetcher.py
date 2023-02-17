import re
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Optional
from xml.etree import ElementTree

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.models import Account, Transaction, TransactionType, TransactionCategory


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

    @staticmethod
    def get_date_to() -> date:
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
        Identifier is an 8-digit number.
        :param string:
        :return: the parsed identifier or None if the identifier was not found
        """
        # Pattern is saying that we are looking for an exactly 8-digit sequence
        # Preceded by start of string, whitespace or colon and followed by end of string, whitespace or comma
        # Example: "IČO: 12345678" or "IČO:12345678" or "12345678 ..."
        pattern = r'(?:^|\s|:)([0-9]{8})(?:$|\s|,)'
        search = re.search(pattern, string)
        return search.group(1) if search is not None else None

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
    def determine_category(transaction: Transaction) -> Optional[TransactionCategory]:
        """
        Determine the category of the transaction.
        It is expected that every transaction fetcher has its own implementation of this method
        and this concrete implementation is called as a fallback when the fetcher does not determine the category.
        :param transaction: Transaction to determine the category for
        :return: category if determined, None otherwise
        """
        # Incoming transaction with a very small amount is considered as a message (probably hateful) for the receiver
        if 1 >= transaction.amount > 0 and transaction.type == TransactionType.INCOMING:
            return TransactionCategory.MESSAGE
        return None

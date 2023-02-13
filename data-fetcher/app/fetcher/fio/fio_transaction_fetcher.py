import re
from datetime import datetime, timedelta
from typing import Optional

import bs4
import requests

from app.fetcher.fio.utils import get_fio_formatted_acc_num
from app.fetcher.transaction_fetcher import TransactionFetcher
from app.models import Transaction, TransactionType, TransactionCategory
from app.utils import float_from_cz


class FioTransactionFetcher(TransactionFetcher):

    URL = 'https://ib.fio.cz/ib/transparent?a={}&f={}&t={}'

    def fetch(self) -> list:
        # Parse account info
        acc_num = get_fio_formatted_acc_num(self.account.number)
        response_text = requests.get(self.URL.format(acc_num, datetime.now().strftime('%d.%m.%Y'), datetime.now().strftime('%d.%m.%Y'))).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        # Set account info
        self.account.name, self.account.balance, self.account.currency = self.scrape_account_info(soup)
        # Parse transactions
        transactions = self.scrape_transactions()
        # Filter out transactions that does not belong to the desired interval
        return list(filter(self.check_date_interval, transactions))

    def scrape_account_info(self, soup: bs4.BeautifulSoup) -> tuple[str, float, str]:
        # Parse name
        name = soup.select_one('.col-md-6 div:nth-child(3)').contents[2].get_text(strip=True)
        # Parse balance and currency
        raw_balance = soup.select_one('.col-md-9 td:nth-child(6)').get_text(strip=True)
        balance, currency = self.parse_money_amount(raw_balance)
        return name, balance, currency

    def scrape_transactions(self) -> list[Transaction]:
        """
        Scrapes all the transactions from the account.
        Fio shows only 2000 transactions at once, so we have to scrape them in intervals.
        Default interval is 1 year, but if there are more than 2000 transactions in the interval,
        we halve the interval and try again.
        """
        acc_num = get_fio_formatted_acc_num(self.account.number)
        date_from = self.get_date_from()
        date_to = self.get_date_to()
        transactions = []

        # Set default scraping interval to 1 year
        interval = timedelta(365)
        while True:
            date_to_current = date_from + interval
            response_text = requests.get(
                self.URL.format(acc_num, date_from.strftime('%d.%m.%Y'), date_to_current.strftime('%d.%m.%Y'))).text
            soup = bs4.BeautifulSoup(response_text, 'html.parser')
            alert = soup.find('div', class_='alert alert-yellow')
            # If there is more than 2000 transactions in the interval, Fio does not show them all and shows an alert
            # In this case, we halve the interval and try again
            if alert is not None:
                interval = interval / 2
                continue
            # Check if there is transaction table to scrape
            no_transactions = soup.find(text='Nejsou dostupné žádné pohyby.')
            if no_transactions is None:
                # We obtain all the transactions in the interval and add them to the list
                rows = soup.find_all('tbody')[1].find_all('tr')
                transactions = transactions + [self.scrape_transaction(row) for row in rows]
            # End of the interval reached
            if date_to_current >= date_to:
                return transactions
            # Update the date_from to the last date we have scraped + 1 day
            date_from = date_to_current + timedelta(1)
            # Reset interval to 1 year
            interval = timedelta(365)

    def scrape_transaction(self, row: bs4.element.Tag) -> Transaction:
        cells = row.find_all('td')

        t_date = datetime.strptime(cells[0].get_text(strip=True), '%d.%m.%Y').date()
        amount, currency = self.parse_money_amount(cells[1].get_text(strip=True))
        t_type = TransactionType.from_float(amount)
        counter_account = cells[3].get_text(strip=True) if t_type == TransactionType.INCOMING else None
        description = cells[4].get_text(strip=True) if t_type == TransactionType.INCOMING else cells[8].get_text(strip=True)
        # Parse the counter account identifier and name
        ca_identifier = self.parse_identifier(description)
        ca_name = self.fetch_identifier_name(ca_identifier) if ca_identifier else None

        transaction = Transaction(
            date=t_date,
            amount=amount,
            currency=currency,
            counter_account=counter_account,
            type=t_type,
            str_type=cells[2].get_text(strip=True),
            variable_symbol=cells[5].get_text(strip=True),
            constant_symbol=cells[6].get_text(strip=True),
            specific_symbol=cells[7].get_text(strip=True),
            description=description,
            ca_identifier=ca_identifier,
            ca_name=ca_name,
            account_number=self.account.number,
            account_bank=self.account.bank
        )
        transaction.category = self.determine_category(transaction)
        return transaction

    @staticmethod
    def parse_money_amount(string: str) -> tuple[float, str]:
        # Parse balance and currency using regex
        pattern = r'(-?[\d\s]+,[\d\s]+) ([A-Z]{3})'
        balance, currency = re.search(pattern, string).groups()
        # Convert from str to corresponding type
        return float_from_cz(balance), currency

    @staticmethod
    def determine_category(transaction: Transaction) -> Optional[TransactionCategory]:
        """
        Determines the category of the transaction.
        :param transaction: Transaction to determine the category for
        :return: category if determined, None otherwise
        """
        # ATM withdrawals
        if transaction.type == TransactionType.OUTGOING and 'Karetní transakce' == transaction.str_type and 'Výběr z bankomatu' in transaction.description:
            return TransactionCategory.ATM
        # Fee
        if transaction.type == TransactionType.OUTGOING and 'Poplatek' in transaction.str_type:
            return TransactionCategory.FEE
        # Tax
        if transaction.type == TransactionType.OUTGOING and 'daně' in transaction.str_type:
            return TransactionCategory.TAX
        # Card payments
        if transaction.type == TransactionType.OUTGOING and 'Karetní transakce' == transaction.str_type:
            return TransactionCategory.CARD
        # Try default category determination
        return TransactionFetcher.determine_category(transaction)

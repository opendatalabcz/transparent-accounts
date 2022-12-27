import re
from datetime import datetime

import bs4
import requests

from ..transaction_fetcher import TransactionFetcher
from .utils import get_html_formatted_acc_num
from ...models import Transaction, TransactionType, Currency


class FioTransactionFetcher(TransactionFetcher):

    URL = 'https://ib.fio.cz/ib/transparent?a={}&f={}t={}'

    def fetch(self) -> list:
        # Get the html page
        acc_num = get_html_formatted_acc_num(self.account.number)
        response_text = requests.get(self.URL.format(acc_num, self.get_date_from(), self.get_date_to())).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        # Set account info
        self.account.name, self.account.balance, self.account.currency = self.scrape_account_info(soup)

        return self.scrape_transactions(soup)

    def scrape_account_info(self, soup: bs4.BeautifulSoup) -> tuple[str, float, Currency]:
        name = soup.select_one('.col-md-6 div:nth-child(3)').get_text(strip=True)
        raw_balance = soup.select_one('.col-md-9 td:nth-child(6)').get_text(strip=True)
        balance, currency = self.parse_money_amount(raw_balance)
        return name, balance, currency

    def scrape_transactions(self, soup: bs4.BeautifulSoup) -> list:
        rows = soup.find_all('tbody')[1].find_all('tr')
        result = []
        for row in rows:
            result.append(self.scrape_transaction(row))

        return result

    def scrape_transaction(self, row: bs4.element.Tag) -> Transaction:
        cells = row.find_all('td')

        t_date = datetime.strptime(cells[0].get_text(strip=True), '%d.%m.%Y').date()
        amount, _ = self.parse_money_amount(cells[1].get_text(strip=True))
        t_type = TransactionType.from_float(amount)
        counter_account = cells[3].get_text(strip=True) if t_type == TransactionType.INCOMING else None
        description = cells[4].get_text(strip=True) if t_type == TransactionType.INCOMING else cells[8].get_text(strip=True)

        return Transaction(
            date=t_date,
            amount=amount,
            counter_account=counter_account,
            type=t_type,
            str_type=cells[2].get_text(strip=True),
            variable_symbol=cells[5].get_text(strip=True),
            constant_symbol=cells[6].get_text(strip=True),
            specific_symbol=cells[7].get_text(strip=True),
            description=description,
            account_number=self.account.number
        )

    @staticmethod
    def parse_money_amount(string: str) -> tuple[float, Currency]:
        # Parse balance and currency using regex
        pattern = r'(-?[\d\s]+,[\d\s]+) ([A-Z]{3})'
        balance, currency = re.search(pattern, string).groups()
        # Replace a comma with a dot, remove fixed spaces and cast to float
        balance = float(balance.replace(',', '.').replace(' ', ''))
        currency = Currency.from_str(currency)

        return balance, currency

import re
from datetime import datetime, date

import bs4
import requests

from app.fetcher.transaction_fetcher import TransactionFetcher
from app.fetcher.fio.utils import get_fio_formatted_acc_num
from app.models import Transaction, TransactionType, Currency
from app.utils import float_from_cz


class FioTransactionFetcher(TransactionFetcher):

    URL = 'https://ib.fio.cz/ib/transparent?a={}&f={}&t={}'

    def fetch(self) -> list:
        # Get the html page
        acc_num = get_fio_formatted_acc_num(self.account.number)
        # Get date interval
        date_from = self.get_date_from().strftime('%d.%m.%Y')
        date_to = self.get_date_to().strftime('%d.%m.%Y')
        response_text = requests.get(self.URL.format(acc_num, date_from, date_to)).text
        soup = bs4.BeautifulSoup(response_text, 'html.parser')
        # Set account info
        self.account.name, self.account.balance, self.account.currency = self.scrape_account_info(soup)

        transactions = self.scrape_transactions(soup)
        # Filter out transactions that does not belong to the desired interval
        # In the case where the date_from is greater than the date_to, Fio does not cooperate
        # and still returns some transactions
        return list(filter(self.check_date_interval, transactions))

    def scrape_account_info(self, soup: bs4.BeautifulSoup) -> tuple[str, float, Currency]:
        # Parse name
        name = soup.select_one('.col-md-6 div:nth-child(3)').contents[2].get_text(strip=True)
        # Parse balance and currency
        raw_balance = soup.select_one('.col-md-9 td:nth-child(6)').get_text(strip=True)
        balance, currency = self.parse_money_amount(raw_balance)
        return name, balance, currency

    def scrape_transactions(self, soup: bs4.BeautifulSoup) -> list[Transaction]:
        rows = soup.find_all('tbody')[1].find_all('tr')
        return [self.scrape_transaction(row) for row in rows]

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
            account_number=self.account.number,
            account_bank=self.account.bank
        )

    @staticmethod
    def parse_money_amount(string: str) -> tuple[float, Currency]:
        # Parse balance and currency using regex
        pattern = r'(-?[\d\s]+,[\d\s]+) ([A-Z]{3})'
        balance, currency = re.search(pattern, string).groups()
        # Convert from str to corresponding type
        return float_from_cz(balance), Currency.from_str(currency)

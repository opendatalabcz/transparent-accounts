from __future__ import annotations
from enum import Enum
from datetime import date, datetime
from typing import Any, Optional
from sqlalchemy import Boolean, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Currency(Enum):
    CZK = 0
    EUR = 1
    USD = 2
    GBP = 3

    @staticmethod
    def from_str(label: str) -> Currency:
        match label.upper():
            case 'CZK':
                return Currency.CZK
            case 'EUR':
                return Currency.EUR
            case 'USD':
                return Currency.USD
            case 'GBP':
                return Currency.GBP
        raise NotImplementedError


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"

    # Max length 16 digits (prefix max 6, separator 1, account number max 10)
    number: Mapped[str] = mapped_column(String(17), primary_key=True)
    # Bank code has fixed length 4 digits
    bank_code: Mapped[str] = mapped_column(String(4))
    name: Mapped[str]
    owner: Mapped[str]
    balance: Mapped[float]
    currency: Mapped[Currency]
    description: Mapped[Optional[str]]
    created: Mapped[Optional[date]]
    last_updated: Mapped[datetime]
    last_fetched: Mapped[Optional[datetime]]
    archived: Mapped[Any] = mapped_column(Boolean, default=False)
    inserted: Mapped[datetime] = mapped_column(default=datetime.now())
    transactions: Mapped[list["Transaction"]] = relationship()

    def __repr__(self) -> str:
        return f"Account({str(self.__dict__)})"


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date]
    amount: Mapped[float]
    counter_account: Mapped[str]
    type: Mapped[str]
    variable_symbol: Mapped[str]
    constant_symbol: Mapped[str]
    specific_symbol: Mapped[str]
    description: Mapped[str]
    account_id: Mapped[int] = mapped_column(ForeignKey("account.number"))

    def __repr__(self) -> str:
        return f"Transaction({str(self.__dict__)})"

from __future__ import annotations
from enum import Enum
from datetime import date, datetime
from typing import Any, Optional
from sqlalchemy import Boolean, String, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Bank(Enum):
    CSAS = '0800'
    FIO = '2010'
    KB = '0100'


class Currency(Enum):
    CZK = 1
    EUR = 2
    USD = 3
    GBP = 4

    @staticmethod
    def from_str(string: str) -> Currency:
        match string.upper():
            case 'CZK':
                return Currency.CZK
            case 'EUR':
                return Currency.EUR
            case 'USD':
                return Currency.USD
            case 'GBP':
                return Currency.GBP
        raise NotImplementedError(f"Unsupported currency: {string}")


class TransactionType(Enum):
    INCOMING = 1,
    OUTGOING = 2

    @staticmethod
    def from_float(num: float) -> TransactionType:
        return TransactionType.INCOMING if num > 0 else TransactionType.OUTGOING


class TransactionCategory(Enum):
    MESSAGE = "Vzkaz"


class UpdateStatus(Enum):
    PENDING = 1
    SUCCESS = 2
    FAILED = 3


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"

    # Fixed length 17 digits (prefix 6, separator 1, account number 10)
    number: Mapped[str] = mapped_column(String(17), CheckConstraint('LENGTH(number) = 17'), primary_key=True)
    bank: Mapped[Bank] = mapped_column(primary_key=True)
    name: Mapped[Optional[str]]
    owner: Mapped[Optional[str]]
    balance: Mapped[Optional[float]]
    currency: Mapped[Optional[Currency]]
    description: Mapped[Optional[str]]
    created: Mapped[Optional[date]]
    last_updated: Mapped[datetime]
    last_fetched: Mapped[Optional[date]]
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
    currency: Mapped[Currency]
    counter_account: Mapped[Optional[str]]
    type: Mapped[TransactionType]
    str_type: Mapped[str]
    variable_symbol: Mapped[str]
    constant_symbol: Mapped[str]
    specific_symbol: Mapped[str]
    description: Mapped[str]
    identifier: Mapped[Optional[str]] = mapped_column(String(8))
    category: Mapped[Optional[TransactionCategory]]
    account_number: Mapped[str]
    account_bank: Mapped[Bank]

    __table_args__ = (ForeignKeyConstraint(["account_number", "account_bank"],
                                           ["account.number", "account.bank"]),
                      {})

    def __repr__(self) -> str:
        return f"Transaction({str(self.__dict__)})"


class AccountUpdate(Base):
    __tablename__ = "account_update"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[UpdateStatus]
    started: Mapped[datetime]
    ended: Mapped[Optional[datetime]]
    account_number: Mapped[str]
    account_bank: Mapped[Bank]

    __table_args__ = (ForeignKeyConstraint(["account_number", "account_bank"],
                                           ["account.number", "account.bank"]),
                      {})

    def __repr__(self) -> str:
        return f"AccountUpdate({str(self.__dict__)})"

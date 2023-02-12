from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Optional

from sqlalchemy import Boolean, String, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Bank(Enum):
    CSAS = '0800'
    CSOB = '0300'
    FIO = '2010'
    KB = '0100'
    MONETA = '0600'
    RB = '5500'


class TransactionType(Enum):
    INCOMING = 1,
    OUTGOING = 2

    @staticmethod
    def from_float(num: float) -> TransactionType:
        return TransactionType.INCOMING if num > 0 else TransactionType.OUTGOING


class TransactionCategory(Enum):
    MESSAGE = "Vzkaz"
    ATM = "Výběr z bankomatu"
    FEE = "Poplatek"
    TAX = "Odvod daně"
    CARD = "Platba kartou"


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
    currency: Mapped[str] = mapped_column(String(20))
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
    currency: Mapped[str] = mapped_column(String(20))
    counter_account: Mapped[Optional[str]] = mapped_column(index=True)
    type: Mapped[TransactionType]
    str_type: Mapped[str]
    variable_symbol: Mapped[str]
    constant_symbol: Mapped[str]
    specific_symbol: Mapped[str]
    description: Mapped[str]
    ca_identifier: Mapped[Optional[str]] = mapped_column(String(8), index=True)
    ca_name: Mapped[Optional[str]]
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

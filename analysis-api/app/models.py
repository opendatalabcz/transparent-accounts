from enum import Enum
from datetime import datetime
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


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    owner: Mapped[str]
    number: Mapped[str] = mapped_column(String(16))  # max length 16 digits (prefix max 6, transaction number max 10)
    bank_code: Mapped[str] = mapped_column(String(4))  # bank code has fixed length 4 digits
    balance: Mapped[float]
    currency: Mapped[Currency]
    description: Mapped[Optional[str]]
    last_updated: Mapped[datetime]
    last_fetched: Mapped[datetime]
    inserted: Mapped[datetime]
    archived: Mapped[Any] = mapped_column(Boolean)
    transactions: Mapped[list["Transaction"]] = relationship()

    def __repr__(self) -> str:
        return f"Account({str(self.__dict__)})"


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    amount: Mapped[float]
    counter_account: Mapped[str]
    type: Mapped[str]
    variable_symbol: Mapped[str]
    constant_symbol: Mapped[str]
    specific_symbol: Mapped[str]
    description: Mapped[str]
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    def __repr__(self) -> str:
        return f"Transaction({str(self.__dict__)})"

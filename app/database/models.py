from datetime import datetime
from typing import List
from sqlalchemy import Integer, Float, BigInteger, DateTime, String, ForeignKey, func
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import SQLALCHEMY_URL


engine = create_async_engine(SQLALCHEMY_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    wealth: Mapped[float] = mapped_column(Float, default=0.0)

    checks: Mapped[List["Check"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    incomes: Mapped[List["Income"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Check(Base):
    __tablename__ = "checks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    datetime = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    sum: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="checks")
    items: Mapped[List["CheckItem"]] = relationship(back_populates="check", cascade="all, delete-orphan")


class CheckItem(Base):
    __tablename__ = "check_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    sum: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String, nullable=True)
    check_id: Mapped[int] = mapped_column(ForeignKey("checks.id"))

    check: Mapped["Check"] = relationship(back_populates="items")


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    sum: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="incomes")


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

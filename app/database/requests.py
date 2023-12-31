from datetime import datetime

from sqlalchemy import select

from app.database.models import User, Check, CheckItem, Income, async_session


async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users


async def get_incomes(offset: int, limit: int):
    async with async_session() as session:
        incomes = await session.scalars(select(Income).offset(offset).limit(limit).order_by(Income.datetime))
        return incomes


async def get_user_by_tg_id(user_tg_id) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_tg_id))
        return user


async def create_user(tg_id: int, wealth: float):
    async with async_session() as session:
        user = User(tg_id=tg_id, wealth=wealth)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def create_income(tg_id: int, _sum: int, desc: str = None, dt: datetime = None):
    async with async_session() as session:
        user = await get_user_by_tg_id(tg_id)
        if user:
            user.wealth += _sum
            income = Income(user=user, sum=_sum, description=desc, datetime=dt)
            session.add(income)
            session.add(user)
            await session.commit()
            await session.refresh(income)
            return income
        else:
            return None


async def create_expense(tg_id: int, _sum: int, desc: str = None, dt: datetime = None):
    async with async_session() as session:
        user = await get_user_by_tg_id(tg_id)
        if user:
            user.wealth -= _sum
            income = Check(user=user, sum=_sum, description=desc, datetime=dt)
            session.add(income)
            session.add(user)
            await session.commit()
            await session.refresh(income)
            return income
        else:
            return None

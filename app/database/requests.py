from sqlalchemy import select

from app.database.models import User, Check, CheckItem, Income, async_session


async def get_users():
    async with async_session() as session:
        users = await session.scalars(select(User))
        return users

import functools

from aiogram import Router, F
from aiogram.types import Message

import app.keyboards as kb
from app.database.requests import get_user_by_tg_id

expenses_router = Router()


@expenses_router.message(F.text == "Expenses")
async def expenses_main(message: Message):
    user = await get_user_by_tg_id(message.from_user.id)

    if user:
        await message.answer(
            f"User {user.tg_id}:\n"
            f"Your wealth = {user.wealth}",
            reply_markup=kb.expenses
        )
    else:
        await message.answer("You are not registered yet! Move your ass to register panel", reply_markup=kb.auth)


@expenses_router.message(F.text == "Available sum")
async def expenses_main(message: Message):
    user = await get_user_by_tg_id(message.from_user.id)

    if user:
        await message.answer(f"Your wealth = {user.wealth}", reply_markup=kb.expenses)
    else:
        await message.answer("You are not registered yet! Move your ass to register panel", reply_markup=kb.auth)

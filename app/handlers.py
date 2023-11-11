from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import app.keyboards as kb

router = Router()


@router.message(F.text == "Get users")
async def users(message: Message):
    await message.answer("Select user", reply_markup=await kb.select_users())


@router.callback_query(F.data.startswith("user_"))
async def user_selected(callback: CallbackQuery):
    user_id = callback.data.split("_")[1]
    await callback.message.answer(f"You choose user with id {user_id}")
    await callback.answer("Selected!")

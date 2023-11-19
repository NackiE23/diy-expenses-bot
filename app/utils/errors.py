from aiogram.types import Message

import app.keyboards as kb


async def user_not_found(message: Message):
    await message.answer("Get outta here. Register first!", reply_markup=kb.auth)


async def incorrect_data(message: Message):
    await message.answer("Not the correct data. Bye!", reply_markup=kb.main)

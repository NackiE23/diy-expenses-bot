from aiogram import Router, F
from aiogram.types import Message

import app.keyboards as kb


weather_router = Router()


@weather_router.message(F.text == "Weather")
async def weather_main(message: Message):
    await message.answer("Select region", reply_markup=kb.weather)

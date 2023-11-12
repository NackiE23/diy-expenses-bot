from aiogram import Router, F
from aiogram.types import Message

import app.keyboards as kb
from app.parsing.sinoptik import get_weather

weather_router = Router()


async def weather_data_to_html(region: str) -> str:
    url, week, today = await get_weather(region)
    html = f"Corresponding url: {url}\n\n"

    for entry in week:
        html += (
            f"<b>{entry.get('day')}</b> (<i>{entry.get('date')}</i>)\n"
            f"{entry.get('description')}\n"
            f"{entry.get('temperature')}\n"
            f"\n"
        )

    return html


@weather_router.message(F.text == "Weather")
async def weather_main(message: Message):
    await message.answer("Select region", reply_markup=kb.weather)


@weather_router.message(F.text == "Lviv")
async def weather_lviv(message: Message):
    html = await weather_data_to_html("львів")
    await message.answer(html)


@weather_router.message(F.text == "Ternopil")
async def weather_ternopil(message: Message):
    html = await weather_data_to_html("тернопіль")
    await message.answer(html)


@weather_router.message(F.text == "Volodymyr")
async def weather_volodymyr(message: Message):
    html = await weather_data_to_html("володимир")
    await message.answer(html)

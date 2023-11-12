import platform
import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BotCommand

from app.database.models import async_main
from app.handlers import router
from app.routers.photo import photo_router
from app.routers.weather import weather_router
from config import TOKEN

import app.keyboards as kb


dp = Dispatcher()
dp.include_routers(router, weather_router, photo_router)

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Hello!", reply_markup=kb.main)


@dp.message(Command("main", "asdf"))
async def cmd_start(message: Message):
    await message.answer("Hi there!", reply_markup=kb.main)


@dp.message(F.text.startswith("command "))
async def answer_message(message: Message):
    # print(await message)
    print(dir(message))
    await message.answer("<b>Yes</b>\nOf courseYes")


async def main():
    await async_main()

    await bot.set_my_commands([
        BotCommand(command="main", description="Main")
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

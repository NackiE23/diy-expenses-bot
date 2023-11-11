import os
import random

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

import app.keyboards as kb

photo_router = Router()


@photo_router.message(F.text == "Random photo")
async def photo_main(message: Message):
    await message.answer("Select region", reply_markup=kb.photo)


@photo_router.message(F.text == "1920x1080")
async def message_high_res(message: Message):
    images = os.listdir("images")
    image = FSInputFile(random.choice(images))
    await message.answer_photo(image)

import os
import random

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

import app.keyboards as kb

photo_router = Router()

image_path = "images\\"
images = []
for path, _, files in os.walk(image_path):
    for name in files:
        images.append(os.path.join(path, name))


@photo_router.message(F.text == "Random photo")
async def photo_main(message: Message):
    await message.answer("Select region", reply_markup=kb.photo)


@photo_router.message(F.text == "1920x1080")
async def message_high_res(message: Message):
    await message.answer_photo(FSInputFile(random.choice(images)))

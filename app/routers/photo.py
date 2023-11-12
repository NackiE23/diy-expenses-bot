import os
import random

import aiohttp
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, URLInputFile

import app.keyboards as kb

photo_router = Router()

image_path = "images\\"
images = []
for path, _, files in os.walk(image_path):
    for name in files:
        images.append(os.path.join(path, name))


@photo_router.message(F.text == "Random photo")
async def photo_main(message: Message):
    await message.answer("Select from you want to get image", reply_markup=kb.photo)


@photo_router.message(F.text == "Local")
async def message_high_res(message: Message):
    await message.answer_photo(FSInputFile(random.choice(images)))


@photo_router.message(F.text == "Unsplash")
async def message_middle_res(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://source.unsplash.com/random/1920x1080", allow_redirects=False) as response:
            if response.status == 302:
                await message.answer_photo(URLInputFile(response.headers.get("Location")))
            else:
                await message.answer_photo(FSInputFile(random.choice(images)))

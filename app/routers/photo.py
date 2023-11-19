import os
import random

import aiohttp
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile

import app.keyboards as kb
from app.utils.google_drive_api import get_random_google_drive_image
from config import IMAGES_PATH

photo_router = Router()
google_drive_image = False

images = []
for path, _, files in os.walk(IMAGES_PATH):
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


@photo_router.message(F.text == "Google Drive")
async def message_random_google_drive_photo(message: Message):
    global google_drive_image

    if google_drive_image:
        await message.answer("Already in use")
    else:
        google_drive_image = True
        await message.answer("This can take an approximately 30 seconds")
        try:
            for _ in range(5):
                random_image = get_random_google_drive_image()
                await message.answer_photo(BufferedInputFile(random_image[0].read(), filename=random_image[1]))
        except:
            pass
        await message.answer("That's all")
        google_drive_image = False

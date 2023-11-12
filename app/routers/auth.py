from aiogram import Router, F
from aiogram.types import Message

import app.keyboards as kb
from app.database.requests import get_user_by_tg_id, create_user

auth_router = Router()


@auth_router.message(F.text == "Auth")
async def auth_main(message: Message):
    await message.answer("Welcome to Auth", reply_markup=kb.auth)


@auth_router.message(F.text == "Registration")
async def auth_main(message: Message):
    user = await get_user_by_tg_id(message.from_user.id)

    if user:
        await message.answer("What are you doing here? Fuck off from this place!", reply_markup=kb.main)
    else:
        user = await create_user(tg_id=message.from_user.id, wealth=0.0)
        if user:
            await message.answer("You have been successfully registered! Now you can use expenses features",
                                 reply_markup=kb.main)
        else:
            await message.answer("I don`t know what`s going wrong, but something goes wrong!")

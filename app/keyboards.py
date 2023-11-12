from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_users

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Expenses")],
    [KeyboardButton(text="Weather")],
    [KeyboardButton(text="Random photo")],
], resize_keyboard=True, input_field_placeholder="Choose option below")

weather = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Ternopil")],
    [KeyboardButton(text="Lviv")],
    [KeyboardButton(text="Volodymyr")],
], resize_keyboard=True)

photo = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Unsplash")],
    [KeyboardButton(text="Local")],
], resize_keyboard=True)


async def select_users():
    users_kb = InlineKeyboardBuilder()
    users = await get_users()
    for user in users:
        users_kb.add(
            InlineKeyboardButton(
                text=f"User id: {user.id}\nUser wealth: {user.wealth}",
                callback_data=f"user_{user.id}"
            )
        )
    return users_kb.adjust(2).as_markup()

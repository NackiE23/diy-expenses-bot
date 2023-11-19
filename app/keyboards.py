from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_users

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Expenses")],
    [KeyboardButton(text="Weather")],
    [KeyboardButton(text="Random photo")],
], resize_keyboard=True, input_field_placeholder="Choose option below")

auth = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Registration")],
], resize_keyboard=True)

expenses_select_action = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Available sum")],
    [KeyboardButton(text="Add expense"), KeyboardButton(text="Add income")],
    [KeyboardButton(text="Get expenses"), KeyboardButton(text="Get incomes")],
    [KeyboardButton(text="Exit")],
], resize_keyboard=True)

add_expense = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Return")]
], resize_keyboard=True)

add_income = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Return")]
], resize_keyboard=True)

get_expanses = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Get 10")],
    [KeyboardButton(text="Return")]
], resize_keyboard=True)

get_incomes = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Get 20")],
    [KeyboardButton(text="Return")]
], resize_keyboard=True)

weather = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Ternopil")],
    [KeyboardButton(text="Lviv")],
    [KeyboardButton(text="Volodymyr")],
], resize_keyboard=True)

photo = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Unsplash")],
    [KeyboardButton(text="Google Drive")],
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

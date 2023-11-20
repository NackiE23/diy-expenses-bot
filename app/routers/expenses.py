from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.keyboards as kb
import app.database.requests as rq
from app.database.models import User
from app.states.expenses import Expenses
from app.utils import errors, validators

expenses_router = Router()


@expenses_router.message(F.text == "Expenses")
@expenses_router.message(Expenses.start)
async def new_expenses_main(message: Message, state: FSMContext):
    user = await rq.get_user_by_tg_id(message.from_user.id)

    if user:
        Expenses.user = user
        await state.set_state(Expenses.select_action)
        await state.update_data(user=user)
        await message.answer(
            f"User {user.tg_id}:\n"
            f"Your wealth = {user.wealth}",
            reply_markup=kb.expenses_select_action
        )
    else:
        await errors.user_not_found(message)


@expenses_router.message(Expenses.select_action)
async def process_action(message: Message, state: FSMContext):
    selected_action = message.text

    if selected_action == "Available sum":
        await available_sum(message)

    elif selected_action == "Add expense":
        await state.set_state(Expenses.add_expense)
        await message.answer("Okay, enter your sum for expense \n"
                             "Regex template: r'^(\\d+(\\.\\d+)?)\\s*(?:-d (.*?))?\\s*(?:-dt (.*?))?$' \n"
                             "Or just example: 203 -d description -dt today \n"
                             "Description (-d) and Datetime (-dt) fields are optional",
                             reply_markup=kb.add_expense)

    elif selected_action == "Add income":
        await state.set_state(Expenses.add_income)
        await message.answer("Okay, enter your sum for income \n"
                             "Regex template: r'^(\\d+(\\.\\d+)?)\\s*(?:-d (.*?))?\\s*(?:-dt (.*?))?$' \n"
                             "Or just example: 203 -d description -dt today \n"
                             "Description (-d) and Datetime (-dt) fields are optional",
                             reply_markup=kb.add_income)

    elif selected_action == "Get expenses":
        await state.set_state(Expenses.get_expenses)
        await message.answer("Expenses menu", reply_markup=kb.get_expanses)

    elif selected_action == "Get incomes":
        await state.set_state(Expenses.get_incomes)
        await message.answer("Incomes menu", reply_markup=kb.get_incomes)

    elif selected_action == "Exit":
        await state.clear()
        await message.answer("Bye", reply_markup=kb.main)

    else:
        await state.clear()
        await errors.incorrect_data(message)


async def available_sum(message: Message):
    user = await rq.get_user_by_tg_id(message.from_user.id)

    if user:
        await message.answer(f"Available sum: {user.wealth}", reply_markup=kb.expenses_select_action)
    else:
        await errors.user_not_found(message)


@expenses_router.message(Expenses.add_expense)
async def add_expense(message: Message, state: FSMContext):
    if message.text == "Return":
        await state.set_state(Expenses.select_action)
        await message.answer("Returned", reply_markup=kb.expenses_select_action)
    else:
        validated_data = validators.input_validation(message.text)

        if validated_data:
            res = await rq.create_expense(
                tg_id=message.from_user.id,
                _sum=validated_data.get('sum'),
                desc=validated_data.get('description'),
                dt=validated_data.get('datetime')
            )

            if res:
                await message.answer(f"Expense added: \n"
                                     f"ID - {res.id} \n"
                                     f"SUM - {res.sum} \n"
                                     f"DESCRIPTION - {res.description} \n"
                                     f"DATETIME - {res.datetime}",
                                     reply_markup=kb.add_expense)
            else:
                await message.answer(f"Something went wrong!", reply_markup=kb.add_expense)
        else:
            await message.answer(f"{message.text} is incorrect value! Use float type instead",
                                 reply_markup=kb.add_expense)


@expenses_router.message(Expenses.add_income)
async def add_income(message: Message, state: FSMContext):
    if message.text == "Return":
        await state.set_state(Expenses.select_action)
        await message.answer("Returned", reply_markup=kb.expenses_select_action)
    else:
        validated_data = validators.input_validation(message.text)

        if validated_data:
            res = await rq.create_income(
                tg_id=message.from_user.id,
                _sum=validated_data.get('sum'),
                desc=validated_data.get('description'),
                dt=validated_data.get('datetime')
            )

            if res:
                await message.answer(f"Income added: \n"
                                     f"ID - {res.id} \n"
                                     f"SUM - {res.sum} \n"
                                     f"DESCRIPTION - {res.description} \n"
                                     f"DATETIME - {res.datetime}",
                                     reply_markup=kb.add_income)
            else:
                await message.answer(f"Something went wrong!", reply_markup=kb.add_income)
        else:
            await message.answer(f"{message.text} is incorrect value! Use float type instead",
                                 reply_markup=kb.add_income)


@expenses_router.message(Expenses.get_expenses)
async def get_expanses(message: Message, state: FSMContext):
    if message.text == "Return":
        await state.set_state(Expenses.select_action)
        await message.answer("Returned", reply_markup=kb.expenses_select_action)
    else:
        user = (await state.get_data())['user']

        if user:
            await message.answer(f"Expenses: *expenses*", reply_markup=kb.get_expanses)
        else:
            await errors.user_not_found(message)


@expenses_router.message(Expenses.get_incomes)
async def get_incomes(message: Message, state: FSMContext):
    if message.text == "Return":
        await state.set_state(Expenses.select_action)
        await message.answer("Returned", reply_markup=kb.expenses_select_action)
    else:
        state_data = await state.get_data()

        user = state_data.get('user')
        incomes_skip = state_data.get('incomes_skip', 0)

        if user:

            await message.answer(f"Incomes: *incomes*", reply_markup=kb.get_incomes)
        else:
            await errors.user_not_found(message)

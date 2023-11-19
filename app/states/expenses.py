from aiogram.fsm.state import StatesGroup, State


class Expenses(StatesGroup):
    start = State()
    select_action = State()
    available_sum = State()
    add_expense = State()
    add_income = State()
    get_incomes = State()
    get_expenses = State()

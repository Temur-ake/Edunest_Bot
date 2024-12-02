from aiogram.fsm.state import State, StatesGroup


class Data(StatesGroup):
    name = State()
    courses = State()
    level = State()
    days = State()
    time = State()
    q_time = State()
    phone_number = State()
    language = State()
    end = State()


class AdminState(StatesGroup):
    title = State()
    photo = State()
    end = State()

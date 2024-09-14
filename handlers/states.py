from aiogram.fsm.state import State, StatesGroup


class Data(StatesGroup):
    name = State()
    sur_name = State()
    email = State()
    phone_number = State()
    language = State()


class AdminState(StatesGroup):
    title = State()
    photo = State()
    end = State()

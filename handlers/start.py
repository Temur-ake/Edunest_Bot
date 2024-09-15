import os
from aiogram import Router, html
from aiogram.filters import CommandStart
# from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from web.models import session, User
from handlers.admin import admin_button
from keyboards import main_button

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    full_name = html.bold(message.from_user.full_name)

    existing_user = session.query(User).filter_by(user_id=user_id).first()
    if not existing_user:
        new_user = User(user_id=user_id)
        session.add(new_user)
        session.commit()

    if user_id == int(os.getenv('ADMIN_ID')):
        await message.answer(
            f'Assalomu alykum admin {full_name}',
            reply_markup=admin_button()
        )
    else:
        await message.answer(
            f"{_('Assalomu alaykum')}, {full_name}\n\n{_('Bizning botga hush kelibsiz')}",
            reply_markup=main_button()
        )

    try:
        data = await state.get_data()
        locale = data.get('locale', 'en')
    except Exception as e:
        print(f"An error occurred while retrieving state data: {e}")
        locale = 'en'

    await state.clear()
    await state.update_data({'locale': locale})

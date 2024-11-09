import asyncio
import os
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from dotenv import load_dotenv
from sqlalchemy import select

from web.models import session, User
from handlers.states import AdminState


def admin_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        KeyboardButton(text=_('Reklama 🔊')),
        KeyboardButton(text="Admin Bo'limi")
    )
    return rkb.as_markup(resize_keyboard=True)


load_dotenv()
admin_router = Router()


@admin_router.message(F.text == "Admin Bo'limi")
async def admin(message: Message):
    link = 'http://k.temur.life:8005'
    await message.answer(text=f"Admin Bo'limi ga o'tish {link}")


@admin_router.message(F.text == "Reklama 🔊", F.from_user.id == int(os.getenv('ADMIN_ID')))
async def admin(message: Message, state: FSMContext):
    await message.answer("Reklama rasmini kiriting !")
    await state.set_state(AdminState.photo)


@admin_router.message(AdminState.photo, F.from_user.id == int(os.getenv('ADMIN_ID')), ~F.text, F.photo)
async def admin(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data({"photo": photo})
    await state.set_state(AdminState.title)
    await message.answer("Reklama haqida to'liq malumot bering !")


@admin_router.message(AdminState.title, F.from_user.id == int(os.getenv('ADMIN_ID')), ~F.photo)
async def admin(message: Message, state: FSMContext):
    title = message.text
    await state.update_data({"title": title})

    data = await state.get_data()
    photo = data.get('photo')
    title = data.get('title')

    await state.clear()

    query_users = select(User.user_id)
    users = session.execute(query_users).scalars().all()

    if not users:
        await message.answer("No users found.")
        return

    tasks = []
    count = 0
    max_tasks_per_batch = 28

    for user_id in users:
        if len(tasks) >= max_tasks_per_batch:
            await asyncio.gather(*tasks)
            tasks = []

        try:
            tasks.append(message.bot.send_photo(chat_id=user_id, photo=photo, caption=title))
            count += 1
        except Exception as e:
            print(f"Error sending message to user {user_id}: {e}")

    if tasks:
        await asyncio.gather(*tasks)

    await message.answer("Reklama yuborildi !", reply_markup=admin_button())
    await state.set_state(AdminState.end)

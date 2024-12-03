import asyncio
import os

from aiogram import Router, html, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils import i18n
from aiogram.utils.i18n import gettext as _

from handlers.admin import admin_button
from keyboards import main_button
from models import session, User

start_router = Router()

CHANNELS = [
    "@TTP_Kurgantepa"
]


async def is_user_subscribed(user_id, bot: Bot):
    not_subscribed_channels = []

    for channel in CHANNELS:
        try:
            status = await bot.get_chat_member(channel, user_id)
            print(f'User {user_id} status in {channel}: {status.status}')
            if status.status not in ['member', 'administrator', 'creator']:
                print(f'User {user_id} is not subscribed to {channel}.')
                not_subscribed_channels.append(channel)
        except Exception as e:
            if "Bad Request: chat not found" in str(e):
                print(
                    f'Could not check subscription for channel {channel}. The channel might be private or the bot does not have permission.')
            not_subscribed_channels.append(channel)

    return not_subscribed_channels


async def get_subscription_check_markup(user_id, bot: Bot):
    inline_buttons = []

    not_subscribed_channels = await is_user_subscribed(user_id, bot)

    for channel in not_subscribed_channels:
        button = InlineKeyboardButton(
            text=f"{channel}",
            url=f"t.me/{channel.strip('@')}"
        )
        inline_buttons.append([button])

    inline_buttons.append([InlineKeyboardButton(text="A'zo bo'ldim ✅", callback_data="start_process")])

    ikb = InlineKeyboardMarkup(inline_keyboard=inline_buttons)
    return ikb


@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    animation = await message.answer(text=f'⏳')
    await asyncio.sleep(1)
    await bot.delete_message(chat_id=message.chat.id, message_id=animation.message_id)

    user_id = message.from_user.id
    full_name = html.bold(message.from_user.full_name)

    await message.answer("Ish boshlanmoqdaa ...", reply_markup=ReplyKeyboardRemove())

    # Check if the user exists in the database
    existing_user = session.query(User).filter_by(user_id=user_id).first()
    if not existing_user:
        new_user = User(user_id=user_id)
        session.add(new_user)
        session.commit()

    not_subscribed_channels = await is_user_subscribed(user_id, bot)

    # Admin check
    if int(message.from_user.id) == int(os.getenv('ADMIN_ID')):
        await message.answer(
            f'Assalomu alaykum admin {full_name}',
            reply_markup=admin_button()
        )

    # Handle subscription or welcome message
    if not not_subscribed_channels:
        # If the user is subscribed to all channels, show the "Azo bo'ldim" button
        await message.answer(
            f'{_("Assalomu alaykum")}, {full_name}\n\n{_("Bizning botga hush kelibsiz")}',
            reply_markup=main_button()
        )
    else:
        markup = await get_subscription_check_markup(user_id, bot)
        await message.answer(_("Assalomu alaykum ! Obuna bo'ling : "), reply_markup=markup)

        await state.set_state('awaiting_subscription')

    # Ensure the default locale is set to 'uz' if the state does not contain a locale
    try:
        data = await state.get_data()
        locale = data.get('locale', 'uz')  # Default to 'uz' if locale is not set
        print(f"Locale for user {user_id}: {locale}")
    except Exception as e:
        print(f'Error fetching locale: {e}')
        locale = 'uz'

    # Update the state and apply locale
    await state.update_data({'locale': locale})

    # Ensure that i18n uses the correct locale for translations
    # This assumes you're using aiogram's i18n system for translation handling
    i18n.current_locale = locale  # Set the locale for i18n translations

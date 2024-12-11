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
                print(f'Could not check subscription for channel {channel}. The channel might be private or the bot does not have permission.')
            not_subscribed_channels.append(channel)

    return not_subscribed_channels

async def get_subscription_check_markup(user_id, bot: Bot):
    inline_buttons = []
    not_subscribed_channels = await is_user_subscribed(user_id, bot)

    # Only create buttons for channels that the user is not subscribed to
    for channel in not_subscribed_channels:
        button = InlineKeyboardButton(
            text=f"Join {channel}",
            url=f"t.me/{channel.strip('@')}"
        )
        inline_buttons.append([button])

    # If there are no not subscribed channels, return an empty markup (no buttons)
    return InlineKeyboardMarkup(inline_keyboard=inline_buttons) if inline_buttons else None

@start_router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    # Animation message to indicate bot is processing
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

    # Check subscription status
    not_subscribed_channels = await is_user_subscribed(user_id, bot)

    # Admin check
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(
            f'Assalomu alaykum admin {full_name}',
            reply_markup=admin_button()
        )
        return

    # If the user is subscribed to all channels, send a welcome message
    if not not_subscribed_channels:
        # Ensure that the locale is set, defaulting to 'uz' if not present
        data = await state.get_data()
        locale = data.get('locale', 'uz')
        await state.update_data({'locale': locale})

        # Set locale for i18n translations
        i18n.current_locale = locale

        await message.answer(
            f'{_("Assalomu alaykum")}, {full_name}\n\n{_("Bizning botga hush kelibsiz")}',
            reply_markup=main_button()
        )
    else:
        # If not subscribed, show a message with subscription links
        markup = await get_subscription_check_markup(user_id, bot)
        if markup:
            await message.answer(_("Assalomu alaykum ! Obuna bo'ling : "), reply_markup=markup)

        await state.set_state('awaiting_subscription')

    # Ensure locale is set correctly in state and i18n
    try:
        data = await state.get_data()
        locale = data.get('locale', 'uz')
        i18n.current_locale = locale
        print(f"Locale for user {user_id}: {locale}")
    except Exception as e:
        print(f'Error fetching locale: {e}')
        locale = 'uz'

    await state.update_data({'locale': locale})

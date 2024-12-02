from aiogram import F
#
# from bot.button.reply import *
# from bot.state import stateup
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import I18n, gettext as _, lazy_gettext as __

from handlers.states import Data
from keyboards import lang_buttons, main_button

language_router = Router()


@language_router.message(F.text == __("🇺🇿/🇷🇺/🇬🇧/ Tilni o'zgaritirish"))
async def language(message: Message, state: FSMContext):
    await state.set_state(Data.language)
    await message.answer(_("Tilni tanlang"), reply_markup=lang_buttons())


@language_router.message(F.text.in_({'🇺🇿 uz', "🇬🇧 en", '🇷🇺 ru', }))
async def language(message: Message, i18n: I18n, state: FSMContext):
    print(message.text)
    lang = message.text.split(' ')[1]
    print(lang)
    await state.update_data({"locale": lang})
    i18n.current_locale = lang
    await message.answer(_("Til o'zgardi ✅"), reply_markup=main_button())


@language_router.message(F.text == __("⬅️ Ortga"))
async def back(message: Message):
    await message.answer(f'{_("Bosh menuga qaytdi ✅")}', reply_markup=main_button())


from aiogram.types import KeyboardButton, WebAppInfo, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        *[
            KeyboardButton(text=_('✅ Malumot qoldirish!')),
            KeyboardButton(text=_('🏢 Biz haqimizda'), web_app=WebAppInfo(url='https://temur.life/')),
            KeyboardButton(text=_("📞 Biz bilan bog'lanish")),
            KeyboardButton(text=_("◀️ Yangilik")),
            KeyboardButton(text=_("🇺🇿/🇷🇺/🇬🇧/ Tilni o'zgaritirish"))
        ]
    )
    rkb.adjust(2, 2)
    return rkb.as_markup(resize_keyboard=True)


def get_phone_number():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        *[
            KeyboardButton(text=_('Telefon raqamni yuborish'), request_contact=True),
        ]
    )
    return rkb.as_markup(resize_keyboard=True)


def yes_no():
    rkb = InlineKeyboardBuilder()
    rkb.add(
        *[
            InlineKeyboardButton(text=_('Ha ✅'), callback_data='1'),
            InlineKeyboardButton(text=_("Yo'q ❌"), callback_data='0')
        ]
    )
    return rkb.as_markup()


def lang_buttons():
    rkb = ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text='🇺🇿 uz'),
        KeyboardButton(text='🇬🇧 en'),
        KeyboardButton(text='🇷🇺 ru'),
        KeyboardButton(text=_('⬅️ Ortga')),
    ])
    rkb.adjust(2)
    return rkb.as_markup(resize_keyboard=True)

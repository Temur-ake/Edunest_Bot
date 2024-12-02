from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from web.models import Course, session, Level


def main_button():
    rkb = ReplyKeyboardBuilder()
    rkb.add(
        *[
            KeyboardButton(text=_('✅ Kursga yozilish !')),
            KeyboardButton(text=_('🔵 Biz ijtimoyi tarmoqlarda')),
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


async def get_courses_keyboard():
    inline_buttons = []

    courses = session.execute(select(Course)).scalars().all()

    for course in courses:
        button = InlineKeyboardButton(
            text=course.name,
            callback_data=f"course_{course.id}"
        )
        inline_buttons.append([button])

    ikb = InlineKeyboardMarkup(inline_keyboard=inline_buttons)

    return ikb


async def get_levels_keyboard(course_id):
    ikb = []

    result = session.execute(select(Level).filter(Level.course_id == course_id))
    levels = result.scalars().all()
    for level in levels:
        d = (InlineKeyboardButton(text=level.name, callback_data=f"level_{level.id}"))
        ikb.append([d])
    ib = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ib


async def get_days_keyboard():
    ikb = []
    days = ['D/CH/J', 'S/P/SH', '5 kun haftada']
    for day in days:
        d = (InlineKeyboardButton(text=day, callback_data=f"day_{day}"))
        ikb.append([d])
    ib = InlineKeyboardMarkup(inline_keyboard=ikb)

    return ib


async def get_times_keyboard():
    ikb = []
    times = ['8:00 - 9:30', '9:30 - 11:00', '14:00 - 15:30', '15:30 - 17:00']
    for time in times:
        d = (InlineKeyboardButton(text=time, callback_data=f"time_{time}"))
        ikb.append([d])
    ib = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ib


async def get_q_times_keyboard():
    ikb = []
    times = ['8:00 - 9:30', '9:30 - 11:00', '14:00 - 15:30', '15:30 - 17:00']
    for time in times:
        d = (InlineKeyboardButton(text=time, callback_data=f"q_time_{time}"))
        ikb.append([d])
    ib = InlineKeyboardMarkup(inline_keyboard=ikb)
    return ib


from sqlalchemy.future import select


# Assuming `data` is a dictionary that contains 'course_id' and 'level_id'
async def get_course_and_level_names(data, session):
    result = session.execute(select(Course).filter(Course.id == data['course_id']))
    course = result.scalars().first()
    if course:
        course_name = course.name
    else:
        course_name = None

    result = session.execute(select(Level).filter(Level.id == data['level_id']))
    level = result.scalars().first()
    if level:
        level_name = level.name
    else:
        level_name = None

    return course_name, level_name

# inform.py
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from handlers.states import Data
from keyboards import main_button, yes_no, get_courses_keyboard, get_levels_keyboard, \
    get_times_keyboard, get_days_keyboard, get_course_and_level_names, get_q_times_keyboard
from models import session

inform_router = Router()


@inform_router.message(F.text == __("✅ Kursga yozilish !"))
async def start(message: Message, state: FSMContext):
    await message.answer(_('Ismingizni kiriting : '))
    await state.set_state(Data.name)


@inform_router.message(Data.name)
async def inform_name(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(_('Kurslardan birini tanlang : '), reply_markup=await get_courses_keyboard())
    await state.set_state(Data.courses)


@inform_router.callback_query(F.data.startswith('course_'))
async def handle_course_selection(callback: CallbackQuery, state: FSMContext):
    course_id = int(callback.data.split('_')[1])
    await state.update_data({'course_id': course_id})
    await callback.message.answer(_('Kurs darajasini tanlang : '), reply_markup=await get_levels_keyboard(course_id))
    await state.set_state(Data.level)


@inform_router.callback_query(F.data.startswith('level_'))
async def handle_level_selection(callback: CallbackQuery, state: FSMContext):
    level_id = int(callback.data.split('_')[1])
    await state.update_data({'level_id': level_id})
    await callback.message.answer(_('Dars kunlarini tanlang : '), reply_markup=await get_days_keyboard())
    await state.set_state(Data.days)


@inform_router.callback_query(F.data.startswith('day_'))
async def handle_day_selection(callback: CallbackQuery, state: FSMContext):
    day = callback.data.split('_')[1]  # D/CH/J or S/P/SH
    await state.update_data({'day': day})
    await callback.message.answer(_('Dars vaqtini tanlang : '), reply_markup=await get_times_keyboard())
    await state.set_state(Data.time)


@inform_router.callback_query(F.data.startswith('time_'))
async def handle_time_selection(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split('_')[1]
    await state.update_data({'time': time})
    await callback.message.answer(_("Qo'shimcha vaqtni  tanlang :"),
                                  reply_markup=await get_q_times_keyboard())
    await state.set_state(Data.q_time)


@inform_router.callback_query(F.data.startswith('q_time_'))
async def handle_time_selection(callback: CallbackQuery, state: FSMContext):
    time = callback.data.split('_')[2]
    await state.update_data({'q_time': time})
    await callback.message.answer(_('Telefon raqamingizni kiriting : Masalan ( 970501655 )'))
    await state.set_state(Data.phone_number)


@inform_router.message(Data.phone_number)
async def handle_phone_number(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number if message.contact else message.text
    await state.update_data({'phone_number': phone_number})

    data = await state.get_data()

    course_name, level_name = await get_course_and_level_names(data, session)

    client_data = (
            f"🔉 Username: @{message.from_user.username}\n"
            f"🫡 {_('Ism')}: {data['name']}\n"
            f"🎓 {_('Kurs')}: {course_name}\n"
            f"📚 {_('Daraja')}: {level_name}\n"
            f"📅 {_('Dars kuni')}: {data['day']}\n"
            f"⏰ {_('Dars vaqti')}: {data['time']}\n"
            f"⏰ " + _("Qo'shimcha Dars vaqti") + f": {data['q_time']}\n"  # Concatenation to avoid backslash in f-string
                                                 f"📞 {_('Telefon raqami')}: {data['phone_number']}"
    )

    await message.answer(_("Malumotlaringiz to\'g\'rimi ?") + f" \n{client_data}", reply_markup=yes_no())


@inform_router.callback_query(F.data == '1')
async def yes(callback: CallbackQuery, bot: Bot, state: FSMContext):
    # Fetch data from the FSM context
    data = await state.get_data()
    course_name, level_name = await get_course_and_level_names(data, session)

    # Create the client data message
    client_data = (
            f"🔉 Username: @{callback.from_user.username}\n"
            f"🫡 {_('Ism')}: {data['name']}\n"
            f"🎓 {_('Kurs')}: {course_name}\n"
            f"📚 {_('Daraja')}: {level_name}\n"
            f"📅 {_('Dars kuni')}: {data['day']}\n"
            f"⏰ {_('Dars vaqti')}: {data['time']}\n"
            f"⏰ " + _("Qo'shimcha Dars vaqti") + f": {data['q_time']}\n"
                                                 f"📞 {_('Telefon raqami')}: {data['phone_number']}"
    )

    # Send the client data to the specified chat
    await bot.send_message(-1002100096917, client_data)

    # Acknowledge the callback query
    await bot.answer_callback_query(callback.id, text=_("Malumotlaringiz yuborildi ✅"))

    # Delete the callback message
    await callback.message.delete()

    # Send confirmation to the user
    await callback.message.answer(_("Malumotlaringiz yuborildi ✅"), reply_markup=main_button())

    # Clear the state and finish the FSM
    await state.finish()  # This clears the state


@inform_router.callback_query(F.data == '0')
async def no(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.message.chat.id, _("Siz proccesni rad etdingiz ❌"), reply_markup=main_button())

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _, lazy_gettext as __

from handlers.states import Data
from keyboards import get_phone_number, yes_no, main_button

inform_router = Router()


@inform_router.message(F.text == __('✅ Malumot qoldirish!'))
async def inform(message: Message, state: FSMContext):
    await message.answer(_('Ismingizni kiriting'))
    await state.set_state(Data.name)


@inform_router.message(Data.name)
async def inform(message: Message, state: FSMContext):
    await state.update_data({'name': message.text})
    await message.answer(_('Familiyangizni kiriting'))
    await state.set_state(Data.sur_name)


@inform_router.message(Data.sur_name)
async def inform(message: Message, state: FSMContext):
    await state.update_data({'sur_name': message.text})
    await message.answer(_('Emailingizni kiriting'))
    await state.set_state(Data.email)


@inform_router.message(Data.email)
async def inform(message: Message, state: FSMContext):
    await state.update_data({'email': message.text})
    await message.answer(_('Telefon raqamingizni kiriting'), reply_markup=get_phone_number())
    await state.set_state(Data.phone_number)


@inform_router.message(Data.phone_number)
async def inform(message: Message, state: FSMContext, bot: Bot):
    await state.update_data({'phone_number': message.contact.phone_number})
    data = await state.get_data()
    lang = data['locale']
    await state.clear()
    await state.update_data({"locale": lang})

    client_data = (f"🔉 Username: @{message.from_user.username}\n"
                   f"🫡 {_('Ism')}: {data['name']}\n"
                   f"🫡 {_('Familiya')}: {data['sur_name']}\n"
                   f"✉️ {_('Email')}: {data["email"]}\n"
                   f"📞 {_('Telefon raqam')}: +{data["phone_number"]}")

    await message.answer(f'{_("Malumotlaringiz to'grimi")} ? \n{client_data}', reply_markup=yes_no())

    @inform_router.callback_query(F.data == '1')
    async def yes(callback: CallbackQuery):
        await bot.send_message(-1002100096917, client_data)
        await callback.message.delete()
        await callback.message.answer(_("Malumotlaringiz yuborildi ✅"), reply_markup=main_button())


@inform_router.callback_query(F.data == '0')
async def no(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.message.chat.id, _("Siz proccesni rad etdingiz ❌"), reply_markup=main_button())

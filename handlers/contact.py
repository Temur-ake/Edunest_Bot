from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from db.models import Contact, session

contact_router = Router()


@contact_router.message(F.text == __("📞 Biz bilan bog'lanish"))
async def inform(message: Message):
    query1 = select(Contact.phone_number1)
    phone_number1 = session.execute(query1).scalars().first()
    query2 = select(Contact.phone_number2)
    phone_number2 = session.execute(query2).scalars().first()
    query3 = select(Contact.email)
    email = session.execute(query3).scalars().first()
    query4 = select(Contact.latitude)
    latitude = session.execute(query4).scalars().first()
    query5 = select(Contact.longtitude)
    longtitude = session.execute(query5).scalars().first()
    query6 = select(Contact.channel)
    channel = session.execute(query6).scalars().first()

    await message.answer(f'{_('🔉 Telegram kanalimiz')}: {channel}\n'
                         f'{_('📞 Telefon raqamimiz')}:  {phone_number1}\n'
                         f'{_('📞 Telefon raqamimiz')}: {phone_number2}\n'
                         f'{_('✉️ Emailimiz')}: {email}\n')
    await message.answer_location(latitude, longtitude)

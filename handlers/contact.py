from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.future import select
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from models import Contact, session

contact_router = Router()

# 📞 Biz bilan bog'lanish handler
@contact_router.message(F.text == __("📞 Biz bilan bog'lanish"))
async def inform(message: Message):
    # Query to get the contact data (just the first one, assuming only one record in DB)
    query = select(Contact)
    result = session.execute(query)  # Use async execute
    contact = result.scalars().first()  # Use .first() to get the first record, not .all()

    if contact:
        response = []
        # Check if the contact fields are not None and append to the response
        if contact.phone_number1:
            response.append(f'{_("📞 Telefon raqamimiz ")} : {contact.phone_number1}')
        if contact.phone_number2:
            response.append(f'{_("📞 Telefon raqamimiz ")} : {contact.phone_number2}')
        if response:
            await message.answer("\n".join(response))
        if contact.latitude and contact.longtitude:
            response.append(f'{_("📍 Lokatsiya")} :')
            await message.answer_location(contact.latitude, contact.longtitude)


    else:
        await message.answer(_("Ma'lumot topilmadi."))  # In case no data found

# 🔵 Biz ijtimoyi tarmoqlarda handler
@contact_router.message(F.text == __('🔵 Biz ijtimoyi tarmoqlarda'))
async def our_social_network(message: Message) -> None:
    query = select(Contact)
    result = session.execute(query)  # Use async execute
    contact = result.scalars().first()  # Use .first() to get the first record

    # Prepare the inline keyboard
    ikb = InlineKeyboardBuilder()

    if contact:
        if contact.instagram_name and contact.instagram_link:
            ikb.row(InlineKeyboardButton(text=contact.instagram_name, url=contact.instagram_link))
        if contact.you_tube_name and contact.you_tube_link:
            ikb.row(InlineKeyboardButton(text=contact.you_tube_name, url=contact.you_tube_link))
        if contact.channel_name and contact.channel_link:
            ikb.row(InlineKeyboardButton(text=contact.channel_name, url=contact.channel_link))
        if contact.channel_name1 and contact.channel_link1:
            ikb.row(InlineKeyboardButton(text=contact.channel_name1, url=contact.channel_link1))

        # Send the social network links to the user
        await message.answer(_('Biz ijtimoiy tarmoqlarda'), reply_markup=ikb.as_markup())
    else:
        await message.answer(_("Ijtimoiy tarmoq ma'lumotlari topilmadi."))  # In case no social network data found

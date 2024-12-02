from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, lazy_gettext as __
from sqlalchemy import select

from models import News, session

news_router = Router()


@news_router.message(F.text == __("◀️ Yangilik"))
async def inform(message: Message):
    query1 = select(News.description)
    description = session.execute(query1).scalars().first()
    query2 = select(News.title)
    title = session.execute(query2).scalars().first()
    query3 = select(News.image)
    image = session.execute(query3).scalars().first()
    query4 = select(News.price)
    price = session.execute(query4).scalars().first()

    d = (f'🔅 {_('Nomi')}: {title}\n'
         f'☝️ {_('Tavsifi')}:  {description}\n'
         f'🤑 {_('Narxi')}: {price}\n')
    await message.answer_photo(photo=image, caption=d)

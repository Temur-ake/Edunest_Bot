import asyncio
import logging
import sys
from os import getenv

from aiogram import *
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.utils.i18n import FSMI18nMiddleware, I18n
from dotenv import load_dotenv

from handlers import dp

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
i18n = I18n(path="locales", default_locale="uz")


async def register_all_middlewares():
    dp.update.middleware(FSMI18nMiddleware(i18n))


async def main() -> None:
    await register_all_middlewares()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())

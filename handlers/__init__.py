from aiogram import Dispatcher

from handlers.admin import admin_router
from handlers.contact import contact_router
from handlers.inform import inform_router
from handlers.languages import language_router
from handlers.news import news_router
from handlers.start import start_router

dp = Dispatcher()
dp.include_routers(*[
    language_router,
    start_router,
    inform_router,
    contact_router,
    news_router,
    admin_router
])

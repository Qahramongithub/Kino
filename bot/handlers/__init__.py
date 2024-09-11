from aiogram import Dispatcher

from bot.handlers.film import film_router
from bot.handlers.start import start_router

dp = Dispatcher()
dp.include_routers(*[
  start_router,
  film_router
])
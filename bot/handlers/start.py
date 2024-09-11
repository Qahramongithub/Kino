from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import html,Router
from sqlalchemy import select, insert

from bot.button.button import kod
from db.modules import User, session

start_router=Router()

@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    query=select(User.id).where(User.user_id==message.from_user.id)
    id=session.execute(query).scalars().first()
    if not id:
        user=insert(User).values(
            user_id=message.from_user.id,
            full_name=message.from_user.full_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
        )
        session.execute(user)
        session.commit()

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer(f"📽Kino kodini kiriting",reply_markup=kod())






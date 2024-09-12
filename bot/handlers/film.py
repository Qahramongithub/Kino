from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.click import PyState
from db.modules import Kino,session
from sqlalchemy import insert,select

film_router=Router()

@film_router.message(F.video)
async def film_handler(message: Message):
    file_id=message.video.file_id
    message_id=message.message_id
    try:
        if message_id and file_id:
            query=insert(Kino).values(file_id=file_id,message_id=message_id)
            session.execute(query)
            session.commit()
            await message.answer(f"🎬Kino kodi {message_id}")
        else:
            await message.answer("Kino saqlanmadi !")
    except Exception as e:
        await message.answer("Bunday kino mavjud !")
@film_router.message(F.text,F.text!="/reklama")
async def film_handler(message: Message,state:FSMContext):
    cod=message.text
    if cod.isdigit():
        query=select(Kino.file_id).where(Kino.message_id==int(cod))
        film_url=session.execute(query).scalars().first()
        if film_url:
            await message.answer_video(video=film_url,caption=f"\n🎞Telegram kanal @kinocom_botuz\n"
                                                              f"\n📥Yuklash kodi {cod}\n")
        else:
            await message.answer("Bunday film yuq !")
    else:
        await state.set_state(PyState.reklama)

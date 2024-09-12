import asyncio
import os
from itertools import cycle

from aiogram import Router, F
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from dotenv import  load_dotenv
from sqlalchemy import select, func

from bot.button.button import back_button
from db.modules import session, User

load_dotenv()

click_rouret=Router()

PY_TOKEN=os.getenv("PAY_TOKEN")

class PyState(StatesGroup):
    pyment=State()
    cliec=State()
    cle=State()
    reklama=State()

class AdminState(StatesGroup):
    photo=State()
    title=State()

@click_rouret.message(F.text=="/reklama")
async  def click_handlers(message:Message,state:FSMContext):
    prices=[
        LabeledPrice(label="Reklama uchun tulov",amount=10000000)
    ]
    await message.answer_invoice(title="Reklama",description="Reklama uchun tulov",payload='1',prices=prices,currency="UZS"
                                 ,provider_token=PY_TOKEN)
    await state.set_state(PyState.cliec)

@click_rouret.message(PyState.cliec)
async def succer_handlers(pre: PreCheckoutQuery,state:FSMContext):
    await pre.answer(True)
    await state.set_state(PyState.cle)
@click_rouret.message(PyState.cle)
@click_rouret.message(lambda message: bool(message.successfull_payment))
async def confirm_handler(message :Message,state:FSMContext):
    if message.successful_payment:
        total_amount=message.successful_payment.total_amount//100
        orser_id=int(message.successful_payment.invoice_payload)
        await message.answer(f"To'lovingiz uchun raxmat\n{total_amount}\n{orser_id}")
        await state.set_state(PyState.pyment)

        await message.answer("Reklama rasmini kiriting !", reply_markup=back_button())
        await state.set_state(AdminState.photo)

@click_rouret.message(AdminState.photo, ~F.text, F.photo,F.vedio)
async def admin(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data({"photo": photo})
    await state.set_state(AdminState.title)
    await message.answer("Reklama haqida to'liq malumot bering !", reply_markup=back_button())


@click_rouret.message(AdminState.title,~F.photo,F.media)
async def admin(message: Message, state: FSMContext):
    title = message.text
    await state.update_data({"title": title})
    tasks = []
    data = await state.get_data()
    await state.clear()
    counts = 0
    users = []
    cnt=0
    query_min = select(func.min(User.id))
    query_max = select(func.max(User.id))

    min_id = session.execute(query_min).scalars().first()
    max_id = session.execute(query_max).scalars().first()
    for i in range(min_id, max_id+1):

        query_user = select(User.user_id).where(User.id == i)
        user = session.execute(query_user).scalars().first()

        users.append(user)
        cnt+=1

    for i in cycle(users):
        a = message
        if counts == cnt:
            break
        if len(tasks) == 28:
            await asyncio.gather(*tasks)
            tasks = []
            try:
                 a = await message.bot.send_photo(chat_id=i, photo=data['photo'], caption=data['title'])
            except:
                pass
        tasks.append(a)
        counts += 1
    await message.answer("Reklama yuborildi !")
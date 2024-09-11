from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder,ReplyKeyboardBuilder
from sqlalchemy import select

from db.modules import Kanal


def subscribed():

        ikb = InlineKeyboardBuilder()

        ikb.add(*[
                InlineKeyboardButton(text="➕Telegram kanal", url=f'https://t.me/kinocom_botuz'),
                InlineKeyboardButton(text="➕Telegram kanal", url=f'https://t.me/pdffileimagebot'),
                InlineKeyboardButton(text="➕Instagram", url=f'https://www.instagram.com/begboyev.q'),
                InlineKeyboardButton(text="✅A'zo", callback_data='azo')
        ])

        return ikb.as_markup()

def kod():
    rkb=ReplyKeyboardBuilder()
    rkb.add(*[
        KeyboardButton(text="Kod",web_app=WebAppInfo(url="https://www.instagram.com/begboyev.q"))
    ])
    return rkb.as_markup(resize_keyboard=True)
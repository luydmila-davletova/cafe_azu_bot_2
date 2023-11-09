from aiogram import Bot
from aiogram.types import Message

from keyboards.inline_keyboards import *
from keyboards.reply_keyboards import *


async def get_start(message: Message, bot: Bot):
    await message.answer('Привет! Я чат-бот сети кафе АЗУ! '
                         'Пожалуйста выберите адрес:',
                         reply_markup=cafe_select_kbd())


async def main_cafe_menu(message: Message, bot: Bot):
    await message.answer('Чем я могу помочь?', reply_markup=main_cafe_kbd())


async def back_to_start(message: Message, bot: Bot):
    await message.answer('Привет! Я чат-бот сети кафе АЗУ! '
                         'Пожалуйста выберите адрес:',
                         reply_markup=cafe_select_kbd())


async def get_contacts(message: Message, bot: Bot):
    await message.answer('***Тут должны быть контакты выбранного кафе***',
                         reply_markup=back_kbd())


async def cafe_menu(message: Message, bot: Bot):
    await message.answer('***Тут должны появляться сеты***',
                         reply_markup=table_or_back_kbd())


async def route_to_cafe(message: Message, bot: Bot):
    await message.answer('***Тут должны быть адреса и геометка***',
                         reply_markup=table_or_back_kbd())


async def date_table(message: Message, bot: Bot):
    await message.answer('Введите дату в формате ДД.ММ (например 02.08)',
                         reply_markup=date_or_back_kbd())


async def person_per_table(message: Message, bot: Bot):
    await message.answer('Укажите количество персон',
                         reply_markup=people_per_table_kbd())


async def name_for_dating(message: Message, bot: Bot):
    await message.answer('На чье имя бронируем стол?',
                         reply_markup=enter_name_kbd())

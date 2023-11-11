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


async def get_name(message: Message, bot: Bot):
    await message.answer(f'{message.from_user.first_name}')
    await message.answer('Введите номер телефона для бронирования стола',
                         reply_markup=enter_phone_kbd())


async def choose_set(message: Message, bot: Bot):
    await message.answer('***Тут появляются сеты для формирования заказа***',
                         reply_markup=go_to_pay_or_choose_food_kbd())


async def get_true_contact(message: Message, bot: Bot, phone: str):
    """Если заказчик правильно указал телефон, то в чат вернется номер."""
    await message.answer(f'{phone}')
    await choose_set(message, bot)


async def get_fake_contact(message: Message, bot: Bot):
    """Если телефон указан неправльно, то в чат вернется ошибка."""
    await message.answer('Вы отправили не свой номер телефона!')


async def check_order_go_to_pay(message: Message, bot: Bot):
    """Клиент проверяет перечень заказанного и переходит к оплате."""
    await message.answer('Вы заказали:\n'
                         '***Тут должно быть перечисление сетов***',
                         reply_markup=check_order_kbd())


async def choose_pay_method(message: Message, bot: Bot):
    """Клиент выбирает способ оплаты сета."""
    await message.answer('Выберите способ оплаты',
                         reply_markup=choose_pay_type_kbd())

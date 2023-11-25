from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.get_sunset import get_sunset_from_api
from keyboards.reply_keyboards import reminder_kbd
from utils.states import StepsForm


async def get_reminder_time(message: Message, bot: Bot, state: FSMContext):
    """Выбор клиентом времени напоминания об ифтаре."""
    await message.answer(
        'Уведомляем Вас, что отмена брони и возврат средств '
        'возможны не менее чем за 3 часа до начала ифтара.\n'
        'За какой период времени до начала ифтара отправить Вам напоминание?',
        reply_markup=reminder_kbd())
    await state.set_state(StepsForm.REMINDER_STATE)


async def three_hours_before_iftar(
        message: Message,
        bot: Bot,
        state: FSMContext,
        apscheduler: AsyncIOScheduler):
    context_data = await state.get_data()
    date = context_data.get('date')
    iftar_time = get_sunset_from_api(date)
    reminder_time = None
    if iftar_time < (datetime.now() + timedelta(hours=3)):
        reminder_time = datetime.now()
    else:
        reminder_time = iftar_time - timedelta(hours=2, minutes=59)
    apscheduler.add_job(
        send_reminder_3_hours,
        trigger='date',
        run_date=reminder_time,
        kwargs={
            'bot': bot, 'chat_id': message.from_user.id, 'state': state
        }
    )


async def send_reminder_3_hours(bot: Bot, chat_id: int, state: FSMContext):
    """Напоминание о предстоящем ифтаре за 3 часа до начала."""
    context_data = await state.get_data()
    name = context_data.get('name')
    address = context_data.get('address')
    date = context_data.get('date')
    person_amount = context_data.get('person_amount')
    text = (
        f'Ассэламуалейкум, {name}!\n'
        f'Напоминаем Вам, что {date} вы забронировали стол '
        f'на {person_amount} человека в кафе A Z U.\n'
        'До начала ифтара осталось менее 3 часов.\n'
        f'Мы ждем Вас по адресу: г. Казань, {address}.')
    await bot.send_message(chat_id=chat_id, text=text)


async def one_day_before_iftar(
        message: Message,
        bot: Bot,
        state: FSMContext,
        apscheduler: AsyncIOScheduler):
    context_data = await state.get_data()
    date = context_data.get('date')
    iftar_time = get_sunset_from_api(date)
    reminder_time = None
    if iftar_time < (datetime.now() + timedelta(days=1)):
        reminder_time = datetime.now()
    else:
        reminder_time = iftar_time - timedelta(days=1)
    apscheduler.add_job(
        send_reminder_1_day,
        trigger='date',
        run_date=reminder_time,
        kwargs={
            'bot': bot, 'chat_id': message.from_user.id, 'state': state
        }
    )


async def send_reminder_1_day(bot: Bot, chat_id: int, state: FSMContext):
    """Напоминание о предстоящем ифтаре за 1 сутки до начала."""
    context_data = await state.get_data()
    name = context_data.get('name')
    address = context_data.get('address')
    date = context_data.get('date')
    person_amount = context_data.get('person_amount')
    text = (
        f'Ассэламуалейкум, {name}!\n'
        f'Напоминаем Вам, что {date} вы забронировали стол '
        f'на {person_amount} человека в кафе A Z U.\n'
        'До начала ифтара осталось менее 24 часов.\n'
        f'Мы ждем Вас по адресу: г. Казань, {address}.')
    await bot.send_message(chat_id=chat_id, text=text)


async def no_reminder(message: Message, bot: Bot, state: FSMContext):
    """Обработчик отсутствия необходимости напоминания."""
    pass

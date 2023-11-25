from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
    apscheduler.add_job(
        send_reminder_3_hours,
        trigger='date',
        run_date=datetime.now() + timedelta(seconds=30),
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
        f'Напоминаем Вам, что {date} вы заказали '
        f'{person_amount} ифтар-сета в кафе A Z U.\n'
        'До начала ифтара осталось 3 часа.\n'
        f'Мы ждем Вас по адресу: г. Казань, {address}.')
    await bot.send_message(chat_id=chat_id, text=text)


async def one_day_before_iftar(
        message: Message,
        bot: Bot,
        state: FSMContext,
        apscheduler: AsyncIOScheduler):
    apscheduler.add_job(
        send_reminder_1_day,
        trigger='date',
        run_date=datetime.now() + timedelta(seconds=20),
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
        f'Напоминаем Вам, что {date} вы заказали '
        f'{person_amount} ифтар-сета в кафе A Z U.\n'
        'До начала ифтара осталось 24 часа.\n'
        f'Мы ждем Вас по адресу: г. Казань, {address}.')
    await bot.send_message(chat_id=chat_id, text=text)


async def no_reminder(message: Message, bot: Bot, state: FSMContext):
    """Обработчик отсутствия необходимости напоминания."""
    pass

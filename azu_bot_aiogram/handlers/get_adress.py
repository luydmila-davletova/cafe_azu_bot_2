from aiogram import Bot
from aiogram.types import Message


async def get_true_adress(message: Message, bot: Bot, adress: str):
    """Если заказчик правильно указал адрес, то в чат вернется адрес кафе."""
    await message.answer(f'{adress}')

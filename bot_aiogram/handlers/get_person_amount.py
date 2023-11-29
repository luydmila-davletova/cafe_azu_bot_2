from aiogram import Bot
from aiogram.types import Message


async def get_true_adress(message: Message, bot: Bot, amount: str):
    """Если клиент корректно указал количество гостей, в чат вернется число"""
    await message.answer(f'{amount}')

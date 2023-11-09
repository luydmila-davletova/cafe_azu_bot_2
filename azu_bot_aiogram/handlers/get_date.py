from aiogram import Bot
from aiogram.types import Message


async def get_true_adress(message: Message, bot: Bot, date: str):
    """Если заказчик корректно указал дату, то в чат вернется дата."""
    await message.answer(f'{date}')

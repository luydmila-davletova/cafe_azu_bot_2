from aiogram import Bot
from aiogram.types import Message


async def get_first_name(message: Message, bot: Bot, first_name: str):
    """Если клиент нажимает кнопку 'На моё имя' - возвращается имя клиента."""
    await message.answer(f'{first_name}')

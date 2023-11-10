from aiogram.types import Message
from aiogram import Bot


async def get_first_name(message: Message, bot: Bot, first_name: str):
    """Если клиент нажимает кнопку 'На моё имя' - возвращается имя клиента."""
    await message.answer(f'{first_name}')

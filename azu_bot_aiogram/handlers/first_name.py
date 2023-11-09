from aiogram import Bot
from aiogram.types import Message
from azu_bot_aiogram.keyboards.reply_keyboards import enter_phone_kbd


async def get_name(message: Message, bot: Bot):
    """Получить имя пользователя для передачи в чат бота по кнопке."""
    await message.answer(f'{message.from_user.first_name}',
                         reply_markup=enter_phone_kbd())

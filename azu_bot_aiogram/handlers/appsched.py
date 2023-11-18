from aiogram import Bot


async def send_reminder(bot: Bot, chat_id: int):
    """Напоминание о предстоящем ифтаре."""
    text = 'До начала ифтара осталось 2 часа. Мы ждем Вас!'
    await bot.send_message(chat_id=chat_id, text=text)

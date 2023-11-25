import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from django.db.migrations import executor

from azu_bot_aiogram.settings import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

dp = Dispatcher(bot)


async def send_notification(message):
    try:
        admin_user = await get_user_model().objects.get(username=settings.ADMIN_USERNAME)
        await bot.send_message(chat_id=admin_user.telegram_chat_id, text=message, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Error sending notification: {e}")


async def on_startup(dp):
    await bot.send_message(chat_id=admin_user.telegram_chat_id, text="Бот запущен")


async def on_shutdown(dp):
    await bot.send_message(chat_id=admin_user.telegram_chat_id, text="Бот выключен")


if __name__ == '__main__':
    from django.contrib.auth import get_user_model
    admin_user = get_user_model().objects.get(username=settings.ADMIN_USERNAME)
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

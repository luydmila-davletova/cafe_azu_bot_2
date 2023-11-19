from aiogram import Bot
from aiogram.fsm.context import FSMContext


async def send_reminder(bot: Bot, chat_id: int, state: FSMContext):
    """Напоминание о предстоящем ифтаре."""
    context_data = await state.get_data()
    name = context_data.get('name')
    address = context_data.get('address')
    text = (
        f'Здравтстуйте, {name}!\n'
        'До начала ифтара осталось 2 часа.\n'
        f'Мы ждем Вас по адресу: г. Казань, {address}')
    await bot.send_message(chat_id=chat_id, text=text)

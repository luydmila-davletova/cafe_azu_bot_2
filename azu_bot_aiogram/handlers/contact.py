from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def get_true_contact(
        message: Message, bot: Bot, phone: str, state: FSMContext
):
    """Если заказчик правильно указал телефон, то в чат вернется номер."""
    await state.update_data(phone=phone)
    await message.answer(f'{phone}')


async def get_fake_contact(message: Message, bot: Bot):
    """Если телефон указан неправльно, то в чат вернется ошибка."""
    await message.answer('Вы отправили не свой номер телефона!')

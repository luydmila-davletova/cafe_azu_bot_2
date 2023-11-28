import re

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers.api import get_cafe, post_quantity


class IsPersonAmount(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности ввода количества человек."""
        pattern = r'^(0?[1-9]|[123][0-9]|4[0])$'
        if re.match(pattern, message.text):
            return {'amount': message.text}
        else:
            return False


class TooManyPersons(BaseFilter):
    async def __call__(
            self, message: Message, bot: Bot, state: FSMContext
    ) -> bool:
        """Проверка числа клиентов для брони столов, если клиентов много."""
        cafes = await get_cafe(bot)
        context_data = await state.get_data()
        address_cafe = context_data.get('address')
        for cafe in cafes:
            if cafe['address'] == address_cafe:
                break
        data_dict = {}
        data_dict['date'] = '-'.join(
            context_data.get('date').split('.')[::-1]
        )
        data_dict['quantity'] = 0
        check_current_cafe = await post_quantity(cafe['id'], data=data_dict)
        free_places = check_current_cafe['quantity']
        if message.text.isdigit() and int(message.text) > int(free_places):
            return {'amount': message.text}
        else:
            return False

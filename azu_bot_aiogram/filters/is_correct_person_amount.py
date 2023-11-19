import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPersonAmount(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности ввода количества человек."""
        pattern = r'[1-4]$'
        if re.match(pattern, message.text):
            return {'amount': message.text}
        else:
            return False


class TooManyPersons(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка числа клиентов для брони столов, если клиентов много."""
        max_table_size = 4
        if message.text.isdigit() and int(message.text) > max_table_size:
            return {'amount': message.text}
        else:
            return False

import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPersonAmount(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности ввода количества человек."""
        pattern = r'[1-6]'
        if re.match(pattern, message.text):
            return {'date': message.text}
        else:
            return False

import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCorrectDate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности ввода даты бронирования."""
        pattern = r'(?<!\d)(?:0?[1-9]|[12][0-9]|3[01]).(?:0?[1-9]|1[0-2])'
        if re.match(pattern, message.text):
            return {'date': message.text}
        else:
            return False

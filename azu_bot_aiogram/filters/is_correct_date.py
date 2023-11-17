from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCorrectDate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности ввода даты бронирования."""
        if (
            bool(datetime.strptime(message.text, '%d.%m.%Y')) and
            (datetime.strptime(message.text, '%d.%m.%Y') >= datetime.now())
        ):
            return {'date': message.text}
        else:
            return False

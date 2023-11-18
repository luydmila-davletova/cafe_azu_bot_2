from datetime import datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCorrectDate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности ввода даты бронирования."""
        today = datetime.now().strftime('%d-%m-%Y')
        if (
            bool(datetime.strptime(message.text, '%d.%m.%Y')) and
            (
                str(datetime.strptime(message.text, '%d.%m.%Y') == today) or
                str(datetime.strptime(message.text, '%d.%m.%Y') > today)
            )
        ):
            return {'date': message.text}
        else:
            return False

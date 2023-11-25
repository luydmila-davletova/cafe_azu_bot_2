from datetime import date, datetime

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsCorrectDate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности ввода даты бронирования."""
        try:
            if bool(datetime.strptime(message.text, '%d.%m.%Y')):
                day, month, year = message.text.split('.')
                incoming_date = date(int(year), int(month), int(day))
                if (
                     incoming_date.strftime('%Y.%m.%d') >=
                     datetime.now().strftime('%Y.%m.%d')):
                    return {'date': message.text}
                else:
                    return False
            else:
                return False
        except ValueError:
            pass

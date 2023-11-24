import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


def get_price(set_number: int):
    """Получить цену по номеру сета."""
    if 1 >= set_number <= 3:
        return 400
    elif 4 >= set_number <= 6:
        return 500
    elif 7 >= set_number <= 9:
        return 700
    else:
        return None


class IsCorrectOrder(BaseFilter):
    """Проверка заказа на корректность."""
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности заказа сетов."""
        set_list = []
        pattern = r'[1-9][/-][1-9]'
        sets = {}
        if message.text is not None:
            if ',' in message.text:
                set_list = message.text.replace(' ', '').split(',')
            else:
                set_list.append(message.text)
            for item in set_list:
                if re.match(pattern, item):
                    set_number, amount = item.split('-')
                    data = {int(set_number): int(amount)}
                    sets.update(data)
                else:
                    return False
            return {'sets': sets}
        else:
            return False

from aiogram.filters import BaseFilter
from aiogram.types import Message

ADRESSES = {
    'ул. Чистопольская, 2',
    'ул. Петербургская, 52',
    'ул. Павлюхина, 91',
    'ул. Петербургская, 14'
}

ALTERNATIVE_ADRESSES = {
    'Чистопольская, 2',
    'Петербургская, 52',
    'Павлюхина, 91',
    'Петербургская, 14'
}


class IsTrueAdress(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности указанного адреса."""
        if message.text in ADRESSES:
            return {'adress': message.text}
        else:
            return False


class IsAnotherCafe(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности указанного адреса."""
        if message.text in ALTERNATIVE_ADRESSES:
            return {'adress': message.text}
        else:
            return False

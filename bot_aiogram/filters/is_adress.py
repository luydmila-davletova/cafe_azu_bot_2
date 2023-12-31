from aiogram.filters import BaseFilter
from aiogram.types import Message
from handlers.api import get_cafe


class IsTrueAdress(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности указанного адреса."""
        cafes = await get_cafe()
        for cafe in cafes:
            if message.text == cafe['address']:
                return {'adress': message.text}
        else:
            return False


class IsAnotherCafe(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка корректности указанного адреса."""
        cafes = await get_cafe()
        for cafe in cafes:
            if message.text == cafe['address']:
                return {'adress': message.text}
        else:
            return False

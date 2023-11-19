from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsTrueName(BaseFilter):
    """Проверка соответствия имени пользователя введённому имени."""
    async def __call__(self, message: Message) -> bool:
        if message.contact.user_id == message.from_user.id:
            return {'first_name': message.from_user.first_name}
        else:
            return False

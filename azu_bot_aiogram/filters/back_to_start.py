from aiogram.filters import BaseFilter
from aiogram.types import Message


MOVE_BACK_COMMANDS = {
    'Вернуться к выбору кафе',
    'Отмена'
}


class GoToStart(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        """Проверка ввода и перенаправление к началу работы бота."""
        if message.text in MOVE_BACK_COMMANDS:
            return {'adress': message.text}
        else:
            return False

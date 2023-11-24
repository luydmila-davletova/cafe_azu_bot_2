from aiogram.filters.callback_data import CallbackData


class SetGroup(CallbackData, prefix='group'):
    size: str


class SetInfo(CallbackData, prefix='iftar'):
    name: str
    price: int

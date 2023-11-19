from aiogram.utils.keyboard import InlineKeyboardBuilder


def food_kbd():
    """Клавиатура для выбора количества порций."""
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='+ 1', callback_data=None)
    keyboard_builder.button(text='- 1', callback_data=None)
#    keyboard_builder.button(text='Продолжить выбор', callback_data=...)
#    keyboard_builder.button(text='Назад')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()

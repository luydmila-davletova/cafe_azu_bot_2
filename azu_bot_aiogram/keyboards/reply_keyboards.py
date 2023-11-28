from aiogram.utils.keyboard import ReplyKeyboardBuilder
from emoji import emojize


def start_kbd():
    """Клавиатура запуска бота."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Начать')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(
        resize_keyboard=True
    )


def back_kbd():
    """Клавиатура возвращения назад."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Назад')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(
        resize_keyboard=True
    )


def cafe_select_kbd(cafes):
    """Клавиатура выбора кафе."""
    keyboard_builder = ReplyKeyboardBuilder()
    for cafe in cafes:
        keyboard_builder.button(text=cafe['address'])
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите адрес кафе.'
    )


def main_cafe_kbd():
    """Основная клавиатура навигации по кафе."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Посмотреть меню')
    keyboard_builder.button(text='Забронировать стол')
    keyboard_builder.button(text='Как добраться')
    keyboard_builder.button(text='Контакты и режим работы')
    keyboard_builder.button(text='Вернуться к выбору кафе')
    keyboard_builder.adjust(2, 2, 1)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Чем я могу помочь?'
    )


def table_or_back_kbd():
    """Перейти к бронированию стола или вернуться назад."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Забронировать стол')
    keyboard_builder.button(text='Назад')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Забронировать стол?'
    )


def reserve_or_back_kbd():
    """Выбрать дату бронирования стола или вернуться назад."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Назад')
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Введите дату в формате ДД.ММ.ГГГГ'
    )


def people_per_table_kbd():
    """Выбрать количество персон или вернуться назад."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='1')
    keyboard_builder.button(text='2')
    keyboard_builder.button(text='3')
    keyboard_builder.button(text='4')
    keyboard_builder.button(text='Назад ' + emojize(':calendar:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Сколько персон будет за столом?'
    )


def move_tables_or_change_cafe_kbd():
    """Сдвигать столы или сменить кафе."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Выбрать другое кафе')
    keyboard_builder.button(text='Назад ' + emojize(':calendar:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Нет подхоящего стола. Как поступим?'
    )


def choose_another_cafe_kbd(cafe_list):
    """Выбрать другое кафе, если в текущем нет столов."""
    keyboard_builder = ReplyKeyboardBuilder()
    for cafe_address in cafe_list:
        keyboard_builder.button(text=cafe_address)
    keyboard_builder.adjust(2)
    keyboard_builder.button(text='Назад ' + emojize(':reverse_button:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите адрес кафе.'
    )


def enter_name_kbd():
    """Отправить имя или вернуться назад."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='На моё имя')
    keyboard_builder.button(text='Назад ' + emojize(':family:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='На какое имя бронируем стол?'
    )


def enter_phone_kbd():
    """Отправить номер телефона или вернуться назад."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(
        text='Отправить мой номер телефона', request_contact=True
    )
    keyboard_builder.button(text='Назад ' + emojize(':left_arrow:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Введите номер телефона.'
    )


def go_to_pay_or_choose_food_kbd():
    """Продолжить выбор еды или перейти к оплате."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Оплатить')
    keyboard_builder.button(text='Назад ' + emojize(':mobile_phone:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Измените заказ или перейдите к оплате.'
    )


def check_order_kbd():
    """Проверить заказ и перейти к оплате."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Перейти к оплате')
    keyboard_builder.button(text='Назад ' + emojize(':pot_of_food:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(1, 2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Проверьте Ваш заказ.'
    )


def choose_pay_type_kbd():
    """Выбрать способ оплаты."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Оплатить через ЮКасса')
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите способ оплаты.'
    )


def no_free_tables_kbd():
    """Появляется в случае отсутствия свободных столов в кафе."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='Выбрать другое кафе')
    keyboard_builder.button(text='Назад ' + emojize(':calendar:'))
    keyboard_builder.button(text='Отмена')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Как поступим?'
    )


def reminder_kbd():
    """Клавиатура выбора периода напоминания о заказе."""
    keyboard_builder = ReplyKeyboardBuilder()
    keyboard_builder.button(text='За сутки')
    keyboard_builder.button(text='За 3 часа')
    keyboard_builder.button(text='Не отправлять напоминание')
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите одну из кнопок.'
    )

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
# from keyboards.inline_keyboards import food_kbd
from keyboards.reply_keyboards import (back_kbd, cafe_select_kbd,
                                       check_order_kbd,
                                       choose_another_cafe_kbd,
                                       choose_pay_type_kbd,
                                       enter_name_kbd, enter_phone_kbd,
                                       go_to_pay_or_choose_food_kbd,
                                       main_cafe_kbd,
                                       move_tables_or_change_cafe_kbd,
                                       people_per_table_kbd,
                                       reserve_or_back_kbd, table_or_back_kbd,)
from utils.states import StepsForm


async def get_start(message: Message, bot: Bot, state: FSMContext):
    """Приветствие и выбор адреса кафе."""
    await message.answer('Привет! Я чат-бот сети кафе АЗУ! '
                         'Пожалуйста выберите адрес:',
                         reply_markup=cafe_select_kbd())
    await state.set_state(StepsForm.CHOOSE_CAFE)


async def main_cafe_menu(message: Message, bot: Bot, state: FSMContext):
    """Главное меню выбранного кафе."""
    await message.answer('Чем я могу помочь?', reply_markup=main_cafe_kbd())
    if message.text.startswith('Назад'):
        pass
    else:
        await state.update_data(address=message.text)
    await state.set_state(StepsForm.CAFE_INFO)


async def back_to_start(message: Message, bot: Bot, state: FSMContext):
    """Переход в начало диалога по кнопке 'Отмена'."""
    await get_start(message, bot, state)
    await state.set_state(StepsForm.CHOOSE_CAFE)


async def back_to_cafe_menu(message: Message, bot: Bot, state: FSMContext):
    """Переход в главное меню кафе по кнопке 'Назад'."""
    await main_cafe_menu(message, bot, state)
    await state.set_state(StepsForm.CAFE_INFO)


async def back_to_date(message: Message, bot: Bot, state: FSMContext):
    """Переход к выбору даты по кнопке 'Назад'."""
    await choose_date(message, bot, state)
    await state.set_state(StepsForm.CHOOSE_DATE)


async def back_to_persons(message: Message, bot: Bot, state: FSMContext):
    """Переход к выбору количества персон по кнопке 'Назад'."""
    await person_per_table(message, bot, state)
    await state.set_state(StepsForm.PERSON_AMOUNT)


async def back_to_name(message: Message, bot: Bot, state: FSMContext):
    """Переход к вводу имени по кнопке 'Назад'."""
    await name_for_reserving(message, bot, state)
    await state.set_state(StepsForm.NAME_STATE)


async def back_to_no_table(message: Message, bot: Bot, state: FSMContext):
    """Переход от выбора альтернативного кафе по кнопке 'Назад'."""
    await no_free_table(message, bot, state)
    await state.set_state(StepsForm.NO_FREE_TABLE)


async def back_to_phone(message: Message, bot: Bot, state: FSMContext):
    """Переход к вводу номера телефона по кнопке 'Назад'."""
    await get_phone(message, bot, state)
    await state.set_state(StepsForm.PHONE_STATE)


async def back_to_set(message: Message, bot: Bot, state: FSMContext):
    """Переход из заказа к началу выбора сетов по кнопке 'Назад'."""
    await choose_set(message, bot, state)
    await state.set_state(StepsForm.ORDER_STATE)


async def get_contacts(message: Message, bot: Bot, state: FSMContext):
    """Страничка контактов выбранного кафе."""
    await message.answer('***Тут должны быть контакты выбранного кафе***',
                         reply_markup=back_kbd())
    await state.set_state(StepsForm.CAFE_ADDRESS)


async def cafe_menu(message: Message, bot: Bot, state: FSMContext):
    """Страничка меню выбранного кафе (до начала бронирования)."""
    await message.answer('***Тут должны появляться сеты***',
                         reply_markup=table_or_back_kbd())
    await state.set_state(StepsForm.MENU_WATCH)


async def route_to_cafe(message: Message, bot: Bot, state: FSMContext):
    """Страничка адреса и геометки выбранного кафе."""
    await message.answer('***Тут должны быть адреса и геометка***',
                         reply_markup=table_or_back_kbd())
    await state.set_state(StepsForm.CAFE_ADDRESS)


async def choose_date(message: Message, bot: Bot, state: FSMContext):
    """Начало бронирования стола. Ввод даты бронирования."""
    await message.answer('Введите дату в формате ДД.ММ (например 02.08.2024)',
                         reply_markup=reserve_or_back_kbd())
    await state.set_state(StepsForm.CHOOSE_DATE)


async def person_per_table(message: Message, bot: Bot, state: FSMContext):
    """Выбор количества персон для брони стола."""
    await message.answer('Укажите количество персон',
                         reply_markup=people_per_table_kbd())
    await state.update_data(date=message.text)
    await state.set_state(StepsForm.PERSON_AMOUNT)


async def name_for_reserving(message: Message, bot: Bot, state: FSMContext):
    """Получение имени для брони стола."""
    await message.answer('На чье имя бронируем стол?',
                         reply_markup=enter_name_kbd())
    if message.text.startswith('Назад'):
        pass
    else:
        await state.update_data(person_amount=message.text)
    await state.set_state(StepsForm.NAME_STATE)


async def get_my_name(message: Message, bot: Bot, state: FSMContext):
    """Получение имени пользователя по кнопке 'На моё имя'."""
    await message.answer(f'{message.from_user.first_name}')
    await state.set_state(StepsForm.NAME_STATE)
    await get_phone(message, bot, state)


async def get_phone(message: Message, bot: Bot, state: FSMContext):
    """Получение номера телефона для брони стола."""
    await message.answer('Введите номер телефона для бронирования стола',
                         reply_markup=enter_phone_kbd())
    if message.text.startswith('Назад'):
        pass
    elif message.text == 'На моё имя':
        await state.update_data(name=message.from_user.first_name)
    else:
        await state.update_data(name=message.text)
    await state.set_state(StepsForm.PHONE_STATE)


async def choose_set(message: Message, bot: Bot, state: FSMContext):
    """Интерактивное меню для оформления заказа с количеством порций."""
    await message.answer('***Тут появляются сеты для формирования заказа***',
                         reply_markup=go_to_pay_or_choose_food_kbd())
    if message.text is not None and not message.text.startswith('Назад'):
        await state.update_data(phone=message.text)
    else:
        pass
    await state.set_state(StepsForm.ORDER_STATE)


async def get_true_contact(
        message: Message, bot: Bot, phone: str, state: FSMContext):
    """Если заказчик правильно указал телефон, то в чат вернется номер."""
    await state.update_data(phone=f'{phone}')
    await message.answer(f'{phone}')
    await choose_set(message, bot, state)


async def get_fake_contact(message: Message, bot: Bot, state: FSMContext):
    """Если телефон указан неправльно, то в чат вернется ошибка."""
    await message.answer('Вы отправили не свой номер телефона!')
    await state.set_state(StepsForm.PHONE_STATE)


async def check_order_go_to_pay(message: Message, bot: Bot, state: FSMContext):
    """Клиент проверяет перечень заказанного и переходит к оплате."""
    context_data = await state.get_data()
    name = context_data.get('name')
    phone = context_data.get('phone')
    date = context_data.get('date')
    person_amount = context_data.get('person_amount')
    address = context_data.get('address')
    await message.answer('Проверьте Ваш заказ:\n'
                         f'Имя: {name}\n'
                         f'Телефон: {phone}\n'
                         f'Дата: {date}\n'
                         f'Адрес: г. Казань, {address}\n'
                         f'Количество гостей: {person_amount}\n'
                         'Вы заказали:\n'
                         '***Тут должно быть перечисление сетов***',
                         reply_markup=check_order_kbd())
    await state.set_state(StepsForm.ORDER_CHECK_PAY)


async def choose_pay_method(message: Message, bot: Bot, state: FSMContext):
    """Клиент выбирает способ оплаты сета."""
    await message.answer('Выберите способ оплаты',
                         reply_markup=choose_pay_type_kbd())
    await state.set_state(StepsForm.PAY_STATE)


async def no_free_table(message: Message, bot: Bot, state: FSMContext):
    """Диалог при отсутствии свободных столов."""
    await message.answer('К сожалению нужного Вам столика нет в наличии.\n'
                         'Можем предложить Вам соединить несколько столов '
                         ' или забронировать стол в другом кафе нашей сети.',
                         reply_markup=move_tables_or_change_cafe_kbd())
    await state.set_state(StepsForm.NO_FREE_TABLE)


async def choose_another_cafe(message: Message, bot: Bot, state: FSMContext):
    """Выбрать кафе со свободными столами запрошенной вместимости."""
    await message.answer(
        '***Тут список кафе со свободными столами запрошенной вместимости***',
        reply_markup=choose_another_cafe_kbd())
    await state.set_state(StepsForm.CHOOSE_ANOTHER_CAFE)

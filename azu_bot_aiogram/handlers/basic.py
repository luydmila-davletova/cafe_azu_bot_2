from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers.api import get_cafe, post_quantity
from handlers.get_free_places import get_free_places
from handlers.media_group import get_media_group, watch_media_group
from handlers.sets_for_order import make_sets
from keyboards.reply_keyboards import (back_kbd, cafe_select_kbd,
                                       check_order_kbd,
                                       choose_another_cafe_kbd,
                                       choose_pay_type_kbd,
                                       enter_name_kbd, enter_phone_kbd,
                                       go_to_pay_or_choose_food_kbd,
                                       main_cafe_kbd,
                                       move_tables_or_change_cafe_kbd,
                                       people_per_table_kbd,
                                       reserve_or_back_kbd, table_or_back_kbd)
from utils.states import StepsForm


async def get_start(message: Message, bot: Bot, state: FSMContext):
    """Приветствие и выбор адреса кафе."""
    cafes = await get_cafe(bot)
    if cafes is None:
        await state.set_state(StepsForm.ERROR)
        await bot_error(message, bot, FSMContext)
    else:
        await message.answer('Ассэламуалейкум!\n'
                             'Я чат-бот сети кафе АЗУ!\n'
                             'Рады будем приготовить для Вас ифтар!\n'
                             'Пожалуйста выберите адрес кафе:',
                             reply_markup=cafe_select_kbd(cafes))
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
    cafes = await get_cafe(bot)
    context_data = await state.get_data()
    address_cafe = context_data.get('address')
    cafe_number = ''
    for cafe in cafes:
        if cafe['address'] == address_cafe:
            break
    cafe_number = cafe['number']
    await message.answer(f'Номер выбранного кафе: {cafe_number}\n'
                         'Режим работы: ежедневно с 9:00 до 20:00',
                         reply_markup=back_kbd())
    await state.set_state(StepsForm.CAFE_ADDRESS)


async def cafe_menu(message: Message, bot: Bot, state: FSMContext):
    """Страничка меню выбранного кафе (до начала бронирования)."""
    await watch_media_group(message, bot)
    await message.answer(
        'Чтобы заказать ифтар-сет, выберите "Забронировать стол".',
        reply_markup=table_or_back_kbd())
    await state.set_state(StepsForm.MENU_WATCH)


async def route_to_cafe(message: Message, bot: Bot, state: FSMContext):
    """Страничка адреса и геометки выбранного кафе."""
    context_data = await state.get_data()
    address = context_data.get('address')
    if address == 'ул. Чистопольская, 2':
        await message.answer_location(
            55.81806843439635, 49.100637931202876,
            reply_markup=table_or_back_kbd())
    elif address == 'ул. Петербургская, 52':
        await message.answer_location(
            55.780572101932165, 49.1340455744581,
            reply_markup=table_or_back_kbd())
    elif address == 'ул. Павлюхина, 91':
        await message.answer_location(
            55.76910772993048, 49.148523032671854,
            reply_markup=table_or_back_kbd())
    else:
        await message.answer_location(
            55.78533167814833, 49.12500099911571,
            reply_markup=table_or_back_kbd())
    await state.set_state(StepsForm.CAFE_ADDRESS)


async def choose_date(message: Message, bot: Bot, state: FSMContext):
    """Начало бронирования стола. Ввод даты бронирования."""
    await message.answer(
        'Введите дату, которую Вы хотите забронировать '
        'в формате ДД.ММ.ГГГГ (например 02.08.2024)',
        reply_markup=reserve_or_back_kbd()
    )
    await state.set_state(StepsForm.CHOOSE_DATE)


async def person_per_table(message: Message, bot: Bot, state: FSMContext):
    """Выбор количества персон для брони стола."""
    if message.text.startswith('Назад'):
        pass
    else:
        await state.update_data(date=message.text)
    cafes = await get_cafe(bot)
    context_data = await state.get_data()
    address_cafe = context_data.get('address')
    for cafe in cafes:
        if cafe['address'] == address_cafe:
            break
    data_dict = {}
    data_dict['date'] = '-'.join(context_data.get('date').split('.')[::-1])
    data_dict['quantity'] = 0
    check_current_cafe = await post_quantity(cafe['id'], data=data_dict)
    free_places = check_current_cafe['quantity']
    await message.answer(
        'Количество свободных мест в этом кафе '
        f'на выбранную дату: {free_places}.\n'
        'Укажите количество гостей.',
        reply_markup=people_per_table_kbd()
    )
    await state.set_state(StepsForm.PERSON_AMOUNT)


async def name_for_reserving(message: Message, bot: Bot, state: FSMContext):
    """Получение имени для брони стола."""
    await message.answer('На чье имя бронируем стол?',
                         reply_markup=enter_name_kbd())
    if message.text.startswith('Назад'):
        pass
    elif message.text.startswith('ул.'):
        await state.update_data(address=message.text)
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
    """Меню для оформления заказа с количеством порций."""
    if message.text is not None and not message.text.startswith('Назад'):
        await state.update_data(phone=message.text)
    else:
        pass
    await get_media_group(message, bot)
    await state.set_state(StepsForm.ORDER_STATE)


async def confirm_order(
    message: Message, bot: Bot, sets: dict, state: FSMContext
):
    """Выводит заказ пользователя в преобразованом виде для проверки."""
    make_sets(sets)
    await state.update_data(total_price=f'{sets["total_price"]}')
    del sets['total_price']
    await state.update_data(data_sets=sets)
    context_data = await state.get_data()
    data_sets_order = context_data.get('data_sets')
    total_price = context_data.get('total_price')
    text = 'Вы выбрали:\n'
    for number, amount in data_sets_order.items():
        text += f'Сет №{number} в количестве {amount} шт.\n'
    text += (
        f'Общая стоимость: {total_price} руб.\n'
        'Чтобы изменить заказ - просто введите здесь новую комбинацию '
        'сетов и их количества.'
    )

    await message.answer(text=text,
                         reply_markup=go_to_pay_or_choose_food_kbd())


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
    data_sets_order = context_data.get('data_sets')
    total_price = context_data.get('total_price')
    text = (
        'Проверьте Ваш заказ:\n'
        f'Имя: {name}\n'
        f'Телефон: {phone}\n'
        f'Дата: {date}\n'
        f'Адрес: г. Казань, {address}\n'
        f'Количество гостей: {person_amount}\n'
    )
    for number, amount in data_sets_order.items():
        text += f'Сет №{number} в количестве {amount} шт.\n'
    text += f'Общая стоимость: {total_price} руб.'
    await message.answer(text=text,
                         reply_markup=check_order_kbd())
    await state.set_state(StepsForm.ORDER_CHECK_PAY)


async def choose_pay_method(message: Message, bot: Bot, state: FSMContext):
    """Клиент выбирает способ оплаты сета."""
    await message.answer('Выберите способ оплаты',
                         reply_markup=choose_pay_type_kbd())
    await state.set_state(StepsForm.PAY_STATE)


async def no_free_table(message: Message, bot: Bot, state: FSMContext):
    """Диалог при отсутствии свободных столов."""
    if message.text.startswith('Назад'):
        pass
    else:
        await state.update_data(person_amount=message.text)
    await message.answer('К сожалению нужного столика нет в наличии.\n'
                         'Можем предложить Вам забронировать стол '
                         'в другом кафе нашей сети.',
                         reply_markup=move_tables_or_change_cafe_kbd())
    await state.set_state(StepsForm.NO_FREE_TABLE)


async def choose_another_cafe(message: Message, bot: Bot, state: FSMContext):
    """Выбрать кафе со свободными столами запрошенной вместимости."""
    cafes = await get_cafe(bot)
    context_data = await state.get_data()
    cafe_list = await get_free_places(cafes, context_data)
    await message.answer(
        'На кнопках ниже представлены адреса кафе с подходящим количеством '
        'свободных столов. \n Пожалуйста выберите адрес.',
        reply_markup=choose_another_cafe_kbd(cafe_list))
    await state.set_state(StepsForm.CHOOSE_ANOTHER_CAFE)


async def wrong_input(message: Message, bot: Bot):
    """Сообщение о некорректном пользовательском вводе."""
    await message.answer(
        'Не могу обработать поступившую информацию, пожалуйста попробуйте '
        'ещё раз. Или перезапустите бота по команде /start')


async def bot_error(message: Message, bot: Bot, state: FSMContext):
    """В случае если появляется ошибки - выдача пользователю сообщения"""
    await message.answer(
        'Технические неполадки, просим обратится по телефону или лично'
    )


async def pay_again_other_cafe(message: Message, bot: Bot, state: FSMContext):
    """Клиент выбирает другое кафе, если нет мест."""
    await state.update_data(address=message.text)
    await message.answer('Выберите способ оплаты',
                         reply_markup=choose_pay_type_kbd())

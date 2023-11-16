from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.inline_keyboards import *
from keyboards.reply_keyboards import *
from utils.states import StepsForm


async def process_back(message: Message, bot: Bot, state: FSMContext):
    """Переход на один уровень вверх по кнопке 'Назад'."""
    current_state = str(await state.get_state())
    previous_state = ''
    if current_state == 'MENU_WATCH' or 'CAFE_ADDRESS':
        previous_state = 'CAFE_INFO'
        await state.set_state(previous_state)
        await main_cafe_menu(message, bot, state)
    elif current_state == 'CHOOSE_DATE':
        previous_state = 'CAFE_INFO'
        await state.set_state(previous_state)
        await main_cafe_menu(message, bot, state)
    elif current_state == 'PERSON_AMOUNT':
        previous_state == 'CHOOSE_DATE'
        await state.set_state(previous_state)
        await reserve_table(message, bot, state)
    elif current_state == 'NAME_STATE':
        previous_state == 'PERSON_AMOUNT'
        await state.set_state(previous_state)
        await person_per_table(message, bot, state)
#    if previous_state:
#        await state.set_state(previous_state)
#        if previous_state == 'CAFE_INFO':
#            await main_cafe_menu(message, bot, state)
#        elif previous_state == 'CHOOSE_DATE':
#            await reserve_table(message, bot, state)
#        elif previous_state == 'PERSON_AMOUNT':
#            await name_for_reserving(message, bot, state)
    else:
        await message.answer('Нет предыдущего шага!')


async def get_start(message: Message, bot: Bot, state: FSMContext):
    """Приветствие и выбор адреса кафе."""
    await message.answer('Привет! Я чат-бот сети кафе АЗУ! '
                         'Пожалуйста выберите адрес:',
                         reply_markup=cafe_select_kbd())
    await state.set_state(StepsForm.CHOOSE_CAFE)


async def main_cafe_menu(message: Message, bot: Bot, state: FSMContext):
    """Главное меню выбранного кафе."""
    await message.answer('Чем я могу помочь?', reply_markup=main_cafe_kbd())
    await state.set_state(StepsForm.CAFE_INFO)


async def back_to_start(message: Message, bot: Bot, state: FSMContext):
    """Переход в начало диалога по кнопке 'Отмена'."""
    await message.answer('Привет! Я чат-бот сети кафе АЗУ! '
                         'Пожалуйста выберите адрес:',
                         reply_markup=cafe_select_kbd())
    await state.set_state(StepsForm.CHOOSE_CAFE)


async def get_contacts(message: Message, bot: Bot):
    """Страничка контактов выбранного кафе."""
    await message.answer('***Тут должны быть контакты выбранного кафе***',
                         reply_markup=back_kbd())


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


async def reserve_table(message: Message, bot: Bot, state: FSMContext):
    """Начало бронирования стола. Ввод даты бронирования."""
    await message.answer('Введите дату в формате ДД.ММ (например 02.08)',
                         reply_markup=reserve_or_back_kbd())
    await state.set_state(StepsForm.CHOOSE_DATE)


async def person_per_table(message: Message, bot: Bot, state: FSMContext):
    """Выбор количества персон для брони стола."""
    await message.answer('Укажите количество персон',
                         reply_markup=people_per_table_kbd())
    await state.set_state(StepsForm.PERSON_AMOUNT)


async def name_for_reserving(message: Message, bot: Bot, state: FSMContext):
    """Получение имени для брони стола."""
    await message.answer('На чье имя бронируем стол?',
                         reply_markup=enter_name_kbd())
    await state.set_state(StepsForm.NAME_STATE)


async def get_name(message: Message, bot: Bot, state: FSMContext):
    """Получение номера телефона для брони стола."""
    await message.answer(f'{message.from_user.first_name}')
    await message.answer('Введите номер телефона для бронирования стола',
                         reply_markup=enter_phone_kbd())
    await state.set_state(StepsForm.PHONE_STATE)


async def choose_set(message: Message, bot: Bot, state: FSMContext):
    """Интерактивное меню для оформления заказа с количеством порций."""
    await message.answer('***Тут появляются сеты для формирования заказа***',
                         reply_markup=go_to_pay_or_choose_food_kbd())
    await state.set_state(StepsForm.ORDER_STATE)


async def get_true_contact(message: Message, bot: Bot, phone: str):
    """Если заказчик правильно указал телефон, то в чат вернется номер."""
    await message.answer(f'{phone}')
    await choose_set(message, bot)


async def get_fake_contact(message: Message, bot: Bot, state: FSMContext):
    """Если телефон указан неправльно, то в чат вернется ошибка."""
    await message.answer('Вы отправили не свой номер телефона!')
    await state.set_state(StepsForm.PHONE_STATE)


async def check_order_go_to_pay(message: Message, bot: Bot, state: FSMContext):
    """Клиент проверяет перечень заказанного и переходит к оплате."""
    await message.answer('Вы заказали:\n'
                         '***Тут должно быть перечисление сетов***',
                         reply_markup=check_order_kbd())
    await state.set_state(StepsForm.ORDER_CHECK_PAY)


async def choose_pay_method(message: Message, bot: Bot):
    """Клиент выбирает способ оплаты сета."""
    await message.answer('Выберите способ оплаты',
                         reply_markup=choose_pay_type_kbd())


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

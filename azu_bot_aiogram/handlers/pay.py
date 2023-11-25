from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery

from handlers.api import get_cafe, post_reservation
from handlers.appsched import get_reminder_time
from settings import settings
from utils.states import StepsForm


async def order(message: Message, bot: Bot, state: FSMContext):
    """Перечень заказа и настройки для оплаты онлайн."""
    context_data = await state.get_data()
    total_price = int(context_data.get('total_price')) * 100
    discount = 0
    if int(total_price) > 50000:
        discount = 50000 - int(total_price)

    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Окно оплаты заказа',
        description='Здесь Вы можете оплатить заказ.',
        payload='Payment through a bot',
        provider_token=settings.bots.provider_token,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Ифтар сеты',
                amount=total_price
            ),
            LabeledPrice(
                label='НДС 20%',
                amount=0,
            ),
            LabeledPrice(
                label='Скидка',
                amount=discount
            )
        ],
        max_tip_amount=None,
        suggested_tip_amounts=None,
        start_parameter='cafe_azu',
        provider_data=None,
        photo_url=None,
        photo_size=None,
        photo_width=None,
        photo_height=None,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=False,
        send_phone_number_to_provider=False,
        send_email_to_provider=False,
        is_flexible=False,
        disable_notification=False,
        protect_content=False,
        reply_to_message_id=None,
        allow_sending_without_reply=True,
        reply_markup=None,
        request_timeout=15
    )


async def pre_checkout_query(
        pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext
):
    """Обработка заказа. Поскольку у нас нет доставки, тут авто согласие."""
    cafes = await get_cafe()
    context_data = await state.get_data()
    address_cafe = context_data.get('address')
    for cafe in cafes:
        if cafe['address'] == address_cafe:
            break
    data_dict = {}
    data_dict['quantity'] = context_data.get('person_amount')
    data_dict['sets'] = [{'sets': 1, 'quantity': 2}]
    data_dict['date'] = '-'.join(context_data.get('date').split('.')[::-1])
    data_dict['name'] = context_data.get('name')
    data_dict['number'] = context_data.get('phone')
    answer = await post_reservation(cafe['id'], data_dict)
    """При неудачной оплате answer['error'] вернет no_places, не уверен куда вести дальше"""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def succesfull_payment(
        message: Message,
        bot: Bot,
        state: FSMContext
):
    """Сообщение об успешной оплате заказа."""
    msg = (
        'Ваш заказ общей стоимостью: '
        f'{message.successful_payment.total_amount // 100} '
        f'{message.successful_payment.currency}. успешно оплачен!'
        f'\r\nСпасибо, что выбираете нас!'
    )
    await message.answer(msg)
    context_data = await state.get_data()
    name = context_data.get('name')
    phone = context_data.get('phone')
    date = context_data.get('date')
    person_amount = context_data.get('person_amount')
    address = context_data.get('address')
    data_sets_order = context_data.get('data_sets')
    total_price = context_data.get('total_price')
    text = (
        'Поступил заказ:\n'
        f'Имя: {name}\n'
        f'Телефон: {phone}\n'
        f'Дата: {date}\n'
        f'Адрес: г. Казань, {address}\n'
        f'Количество гостей: {person_amount}\n'
    )
    for number, amount in data_sets_order.items():
        text += f'Сет №{number} в количестве {amount} шт.\n'
    text += f'Общая стоимость: {total_price} руб.'
    await bot.send_message(chat_id=settings.bots.admin_id, text=text)
    await state.set_state(StepsForm.FINAL_STATE)
    await get_reminder_time(message, bot, state)

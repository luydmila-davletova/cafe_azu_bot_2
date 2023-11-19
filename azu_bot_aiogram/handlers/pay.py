from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, Message, PreCheckoutQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.appsched import send_reminder
from settings import settings
from utils.states import StepsForm


async def order(message: Message, bot: Bot, state: FSMContext):
    """Перечень заказа и настройки для оплаты онлайн."""
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Окно оплаты заказа',
        description='Здесь Вы можете оплатить заказ.',
        payload='Payment through a bot',
        provider_token=settings.bots.provider_token,
        currency='rub',
        prices=[
            LabeledPrice(
                label='Сет №1',
                amount=10000
            ),
            LabeledPrice(
                label='НДС 20%',
                amount=0,
            ),
            LabeledPrice(
                label='Сет №9',
                amount=20000
            ),
            LabeledPrice(
                label='НДС 20%',
                amount=0,
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


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    """Обработка заказа. Поскольку у нас нет доставки, тут авто согласие."""
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def succesfull_payment(
        message: Message,
        bot: Bot,
        state: FSMContext,
        apscheduler: AsyncIOScheduler
):
    """Сообщение об успешной оплате заказа."""
    msg = (
        'Ваш заказ общей стоимостью: '
        f'{message.successful_payment.total_amount // 100} '
        f'{message.successful_payment.currency}. успешно оплачен!'
        f'\r\nЗа 2 часа до начала ифтара мы пришлем Вам напоминание.'
        f'\r\nСпасибо! Хорошего дня!'
    )
    await message.answer(msg)
    await state.set_state(StepsForm.FINAL_STATE)
    print(datetime.now())
    apscheduler.add_job(
        send_reminder,
        trigger='date',
        run_date=datetime.now() + timedelta(seconds=10),
        kwargs={
            'bot': bot, 'chat_id': message.from_user.id, 'state': state
        }
    )

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command

from filters.back_to_start import GoToStart
from filters.is_adress import IsTrueAdress, IsAnotherCafe
from filters.is_contact import IsTrueContact
from filters.is_correct_date import IsCorrectDate
from filters.is_correct_person_amount import IsPersonAmount, TooManyPersons
from handlers.basic import (back_to_start, cafe_menu,
                            check_order_go_to_pay, choose_another_cafe,
                            choose_pay_method, choose_set, reserve_table,
                            get_contacts, get_name, get_start,
                            get_fake_contact, get_true_contact,
                            main_cafe_menu, name_for_reserving,
                            no_free_table, person_per_table, route_to_cafe)
from handlers.pay import order, pre_checkout_query, succesfull_payment
from settings import settings


async def start():
    """Функция, запускающая работу бота."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()
    dp.message.register(order, F.text == 'Оплатить через ЮКасса')
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(succesfull_payment, F.successful_payment)
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_fake_contact, F.contact)
    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(main_cafe_menu, IsTrueAdress())
    dp.message.register(back_to_start, GoToStart())
    dp.message.register(get_contacts, F.text == 'Контакты и режим работы')
    dp.message.register(cafe_menu, F.text == 'Посмотреть меню')
    dp.message.register(route_to_cafe, F.text == 'Как добраться')
    dp.message.register(reserve_table, F.text =='Забронировать стол')
    dp.message.register(person_per_table, IsCorrectDate())
    dp.message.register(name_for_reserving, IsPersonAmount())
    dp.message.register(choose_another_cafe, F.text == 'Выбрать другое кафе')
    dp.message.register(name_for_reserving, F.text == 'Сдвигать столы')
    dp.message.register(name_for_reserving, IsAnotherCafe())
    dp.message.register(no_free_table, TooManyPersons())
    dp.message.register(get_name, F.text == 'На моё имя')
    dp.message.register(choose_set, F.text.startswith('+79'))
    dp.message.register(check_order_go_to_pay, F.text == 'Оплатить')
    dp.message.register(choose_pay_method, F.text == 'Перейти к оплате')


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())

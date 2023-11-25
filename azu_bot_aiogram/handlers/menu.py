from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.callback_setup import SetGroup, SetInfo
from keyboards.inline_keyboards import cart, catalog, catalog_set400, catalog_set500, catalog_set700


sets = [
    {'title': 'Сет № 1', 'price': 400},
    {'title': 'Сет № 2', 'price': 400},
    {'title': 'Сет № 3', 'price': 400},
    {'title': 'Сет № 4', 'price': 500},
    {'title': 'Сет № 5', 'price': 500},
    {'title': 'Сет № 6', 'price': 500},
    {'title': 'Сет № 7', 'price': 700},
    {'title': 'Сет № 8', 'price': 700},
    {'title': 'Сет № 9', 'price': 700},
]

order = {}

def addItem(order, item, price):
    if order is False:
        data = '{"%s":{"count":1}, "all_price":%d}' % (item, price)
        order.update(data)
        return order

    order["all_price"] += price
    if item in order.keys():
        order[item]["count"] += 1        
        return order

    order.update({item:{"count":1}})
    return order


def delItem(order, item, price):
    if order is False:
        return False

    if item in order.keys():
        order["all_price"] -= price
        if order[item]["count"] > 1:
            order[item]["count"] -= 1
            return order
        del order[item]        
        return order

    return False


def user_cart(order):
	text = "Ваша корзина пуста"
	if order is not False:
		text = "В Вашей корзине на данный момент:\n\n"
		text += "<b>Итоговая сумма: {price}</b>\n\n".format(price=order["all_price"])
		del order["all_price"]
		for item in order:
			text += "{item} {count}шт\n".format(item=item, count=order[item]["count"])
	return text


def user_confirm_order(order):
	if order is False:
		return False
	text = "Ваш заказ:\n\n"
	text += "<b>Итоговая сумма: {price}</b>\n\n".format(price=order["all_price"])
	del order["all_price"]
	for item in order:
		text += "{item} {count}шт\n".format(item=item, count=order[item]["count"])
	return text


async def view_catalog(message: Message, bot: Bot, state: FSMContext):
    await message.answer('Выберите ценовую категорию сета', reply_markup = catalog)


async def back_to_catalog(call: CallbackQuery, bot: Bot, callback_data: SetGroup):
    await bot.send_message('Выберите ценовую категорию сета', reply_markup = catalog())
    await call.answer()
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.callback_setup import SetGroup, SetInfo


def cart(user_cart):
    """Главная клавиатура меню сетов."""
    keyboard = InlineKeyboardMarkup()
    if user_cart is not False:
        keyboard.add(
            InlineKeyboardButton(text='✅ Оформить', callback_data='checkout')
        )
    keyboard.add(
        InlineKeyboardButton(text='💰 Каталог', callback_data='catalog')
    )
    return keyboard


def catalog():
    """Клавиатура каталога выбора сетов."""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Сеты за 400 рублей', callback_data=SetGroup(size='small')
        ),
        InlineKeyboardButton(
            text='Сеты за 500 рублей', callback_data=SetGroup(size='medium')
        ),
        InlineKeyboardButton(
            text='Сеты за 700 рублей', callback_data=SetGroup(size='large')
        ),
    )
    return keyboard


def catalog_set400():
    """Клавиатура сетов за 400 рублей."""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text='Сет №1', callback_data=SetInfo(name='Сет №1', price=400)),
        InlineKeyboardButton(text='Cет №2', callback_data=SetInfo(name='Сет №2', price=400)),
        InlineKeyboardButton(text='Cет №3', callback_data=SetInfo(name='Сет №3', price=400)),
    )
    keyboard.add(
        InlineKeyboardButton(text='Корзина', callback_data='go_to_cart')
    )
    keyboard.add(
        InlineKeyboardButton(text='Вернуться', callback_data=SetGroup(size='small'))
    )
    return keyboard


def catalog_set500():
    """Клавиатура сетов за 500 рублей."""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text='Сет №4', callback_data=SetInfo(name='Сет №4', price=500)),
        InlineKeyboardButton(text='Cет №5', callback_data=SetInfo(name='Сет №5', price=500)),
        InlineKeyboardButton(text='Cет №6', callback_data=SetInfo(name='Сет №6', price=500)),
    )
    keyboard.add(
        InlineKeyboardButton(text='Корзина', callback_data='go_to_cart')
    )
    keyboard.add(
        InlineKeyboardButton(text='Вернуться', callback_data=SetGroup(size='medium'))
    )
    return keyboard


def catalog_set700():
    """Клавиатура сетов за 700 рублей."""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text='Сет №7', callback_data=SetInfo(name='Сет №7', price=700)),
        InlineKeyboardButton(text='Cет №8', callback_data=SetInfo(name='Сет №8', price=700)),
        InlineKeyboardButton(text='Cет №9', callback_data=SetInfo(name='Сет №9', price=700)),
    )
    keyboard.add(
        InlineKeyboardButton(text='Корзина', callback_data='go_to_cart')
    )
    keyboard.add(
        InlineKeyboardButton(text='Вернуться', callback_data=SetGroup(size='large'))
    )
    return keyboard


def item_add(user_cart, callback_data: SetInfo):
    """Клавиатура для корзины - добавить/убрать сет."""
    item = callback_data.name
    price = callback_data.price
    if price == 400:
        catalog_tag = 'small'
    elif price == 500:
        catalog_tag = 'medium'
    else:
        catalog_tag = 'large'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Добавить',
            callback_data='add_{item}_{price}'.format(
                item=item, price=price
            )
        ),
        InlineKeyboardButton(
            text='Убрать',
            callback_data='del_{item}_{price}'.format(
                item=item, price=price
            )
        ),
    )
    if user_cart is not False:
        keyboard.add(
            InlineKeyboardButton(
                text='Корзина', callback_data='go_to_cart'
            ),
            InlineKeyboardButton(
                text='✅ Оформить', callback_data='checkout'
            )
        )
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться', callback_data='catalog_{tag}'.format(
                tag=catalog_tag
            )
        )
    )
    return keyboard

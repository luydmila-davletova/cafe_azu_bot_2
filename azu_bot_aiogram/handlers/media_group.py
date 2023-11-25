from aiogram import Bot
from aiogram.types import FSInputFile, InputMediaPhoto, Message


async def get_media_group(message: Message, bot: Bot):
    set_1 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set1.jpg'),
        caption=('Выберите сеты для ифтара и введите в формате '
                 'номер сета - количество сетов в заказе, например, '
                 '"1-1, 2-3" - это означает, что Вы выбрали 1 сет №1 и '
                 '3 сета № 2.')
    )
    set_2 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set2.jpg')
    )
    set_3 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set3.jpg')
    )
    set_4 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set4.jpg')
    )
    set_5 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set5.jpg')
    )
    set_6 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set6.jpg')
    )
    set_7 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set7.jpg')
    )
    set_8 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set8.jpg')
    )
    set_9 = InputMediaPhoto(
        type='photo', media=FSInputFile(r'images/set9.jpg')
    )
    media = [set_1, set_2, set_3, set_4, set_5, set_6, set_7, set_8, set_9]
    await message.answer_media_group(media)

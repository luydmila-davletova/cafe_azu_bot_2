from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='cancel',
            description='Сбросить'
        ),
        BotCommand(
            command='inline',
            description='Показать инлайн клавиатуру'
        ),
        BotCommand(
            command='pay',
            description='Купить продукт'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())

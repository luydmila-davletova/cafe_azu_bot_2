import json
from channels.generic.websocket import AsyncWebsocketConsumer
from aiogram import Bot, Dispatcher
from azu_bot_django import settings


class AiogramConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.bot = Bot(token=settings.bots.bot_token)
        self.dp = Dispatcher(self.bot)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(
            text_data=json.dumps(
                {'response': 'Сообщение успешно получено.'}))
        await self.bot.send_message(
            chat_id=settings.bots.admin_id, text=message)

    async def aiogram_message_handler(self, event):
        message = event.message.text
        await self.send(text_data=json.dumps({'aiogram_message': message}))

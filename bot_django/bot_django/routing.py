from django.urls import re_path

from bot_django import consumers

websocket_urlpatterns = [
    re_path(r'ws/telegram/$', consumers.AiogramConsumer.as_asgi()),
]

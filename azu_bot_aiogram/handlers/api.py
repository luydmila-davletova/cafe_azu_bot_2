import aiohttp
from settings import django_token, settings


async def get_session():
    session = aiohttp.ClientSession(
        headers={"Authorization": f'Token {django_token}'}
    )
    return session


async def get_cafe(bot=None):
    mysession = await get_session()
    async with mysession as session:
        async with session.get(
            'http://127.0.0.1:8000/cafes/'
        ) as response:
            response = await response.json()
            if not isinstance(response, list):
                await bot.send_message(
                    chat_id=settings.bots.admin_id,
                    text='Нет связи с базой данных!'
                    'Проверьте валидность django token!')
                return None
            return response


async def post_quantity(cafe, data):
    mysession = await get_session()
    async with mysession as session:
        async with session.post(
            f'http://127.0.0.1:8000/cafes/{cafe}/quantity/', json=data
        ) as response:
            return await response.json()


async def post_reservation(cafe_id, data):
    mysession = await get_session()
    async with mysession as session:
        async with session.post(
            f'http://127.0.0.1:8000/cafes/{cafe_id}/reservations/', json=data
        ) as response:
            return await response.json()

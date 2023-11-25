import aiohttp
from settings import django_token

async def get_cafe():
    async with aiohttp.ClientSession(headers={"Authorization": f'Token {django_token}'}) as session:
        async with session.get('http://127.0.0.1:8000/cafes') as response:
            return await response.json()

async def post_reservation(cafe_id, data):
    async with aiohttp.ClientSession(headers={"Authorization": f'Token {django_token}'}) as session:
        async with session.post(f'http://127.0.0.1:8000/cafes/{cafe_id}/reservations/', json=data) as response:
            return await response.json()
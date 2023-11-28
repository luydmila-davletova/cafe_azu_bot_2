import aiohttp


async def get_cafe(bot=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            'http://backend:8000/cafes/'
        ) as response:
            return await response.json()


async def get_cafe_admins(cafe):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'http://backend:8000/cafes/{cafe}/admins/'
        ) as response:
            return await response.json()


async def post_quantity(cafe, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'http://backend:8000/cafes/{cafe}/quantity/', json=data
        ) as response:
            return await response.json()


async def post_reservation(cafe_id, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'http://backend:8000/cafes/{cafe_id}/reservations/', json=data
        ) as response:
            return await response.json()

from datetime import datetime

import requests

SUNSET_API = (
    'https://api.sunrisesunset.io/json?lat=55.78874&lng=49.12214&date='
)


def get_sunset_from_api(date):
    """Получаем время захода солнца в выбраный день."""
    response = requests.get(SUNSET_API + str(date))
    data = response.json()
    sunset_of_day = data['results']['sunset']
    date = datetime.strptime(date, '%d.%m.%Y')
    sunset_of_day = datetime.strptime(sunset_of_day, '%I:%M:%S %p')
    sunset_of_day = sunset_of_day.replace(
        year=date.year, month=date.month, day=date.day
    )
    return sunset_of_day

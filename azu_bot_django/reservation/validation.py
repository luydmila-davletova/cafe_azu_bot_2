from django.core.exceptions import ValidationError
import requests
from datetime import datetime

from reservation.models import Reservation

SUNSET_API = 'https://api.sunrisesunset.io/json?lat=55.78874&lng=49.12214'


def tables_in_cafe(reservation_data):
    tables_pk = reservation_data['table']
    for table in tables_pk:
        if reservation_data['cafe'].id != table.cafe.id:
            raise ValidationError(
                'Кафе и столы в кафе должны совпадать по местоположению'
            )


def tables_in_cafe_in_date(reservation_data):
    tables_pk = reservation_data['table']
    for table in tables_pk:
        if Reservation.objects.filter(
            cafe=reservation_data['cafe'],
            table=table,
            date=reservation_data['date'],
            status=1,
        ):
            raise ValidationError(
                'Активная бронь с этим столом на эту дату существует'
            )


def tables_available(reservation_data):
    tables = reservation_data['table']
    date = reservation_data['date']
    cafe = reservation_data['cafe']
    unailable_tables = Reservation.table.through.objects.filter(
        reservation__cafe__id=cafe.id,
        reservation__date=date,
        reservation__status='booked'
    ).values('table')
    if tables.filter(id__in=unailable_tables):
        raise ValidationError(
            'Выбранные столы уже заняты на это число!'
        )


# def cancell_reservation(data, rus=False):
#     reservation_date = data['date'].value
#     reservation_date = datetime.strptime(reservation_date, '%Y-%m-%d')
#     today = datetime.now()
#     if reservation_date == today:
#         rus = True
#     sunset_time = get_sunset_from_api()
#     raise ValidationError(
#         rus
#     )


# def get_sunset_from_api():
#     """Получаем время захода солнца"""
#     try:
#         response = requests.get(SUNSET_API)
#     except requests.ConnectionError:
#         raise ValidationError(
#             {'status': 'error',
#              'message': 'Ошибка при получении времени заката!'}
#         )
#     data = response.json()
#     if data['status'] != 'OK':
#         raise ValidationError(
#             {'status': 'error',
#              'message': 'Нет возможности проверить время заката!'}
#         )
#     sunset_today = data['results']['sunset']
#     today = datetime.today()
#     sunset_today = datetime.strptime(sunset_today, '%I:%M:%S %p')
#     sunset_today = sunset_today.replace(
#         year=today.year, month=today.month, day=today.day
#     )
#     return sunset_today

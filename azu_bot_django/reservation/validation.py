from datetime import date, datetime, timedelta

import requests
from django.core.exceptions import ValidationError
from rest_framework import serializers

from reservation.models import Reservation

SUNSET_API = 'https://api.sunrisesunset.io/json?lat=55.78874&lng=49.12214'


def tables_in_cafe(form_model):
    reservation_data = form_model.cleaned_data
    tables_pk = reservation_data['table']
    for table in tables_pk:
        if reservation_data['cafe'].id != table.cafe.id:
            raise ValidationError(
                'Кафе и столы в кафе должны совпадать по местоположению'
            )


def tables_in_cafe_in_date(form_model):
    reservation_data = form_model.cleaned_data
    reservation_id = form_model.instance.id
    tables_pk = reservation_data['table']
    for table in tables_pk:
        if Reservation.objects.filter(
            cafe=reservation_data['cafe'],
            table=table,
            date=reservation_data['date'],
            status=1,
        ).exclude(id=reservation_id):
            raise ValidationError(
                'Активная бронь с этим столом на эту дату существует'
            )


def tables_available(form_model):
    reservation_data = form_model.cleaned_data
    reservation_id = form_model.instance.id
    tables = reservation_data['table']
    date = reservation_data['date']
    cafe = reservation_data['cafe']
    unailable_tables = Reservation.table.through.objects.filter(
        reservation__cafe__id=cafe.id,
        reservation__date=date,
        reservation__status='booked'
    ).exclude(reservation=reservation_id).values('table')
    if tables.filter(id__in=unailable_tables):
        raise ValidationError(
            'Выбранные столы уже заняты на это число!'
        )


"""Валидаторы для сериализаторов"""


def cancell_reservation(data, rus=False):
    reservation_date = data['date'].value
    reservation_date = date.fromisoformat(reservation_date)
    today = date.today()
    if data['status'].value == 'cancelled':
        return
    if reservation_date == today:
        time_until_cancellation = get_sunset_from_api() - timedelta(hours=2)
        if time_until_cancellation < datetime.now():
            raise serializers.ValidationError(
                {'status': 'error',
                 'message': 'Отменить менее чем за два часа до брони нельзя!'}
            )


def get_sunset_from_api():
    """Получаем время захода солнца"""
    try:
        response = requests.get(SUNSET_API)
    except requests.ConnectionError:
        raise serializers.ValidationError(
            {'status': 'error',
             'message': 'Ошибка при получении времени заката!'}
        )
    data = response.json()
    if data['status'] != 'OK':
        raise serializers.ValidationError(
            {'status': 'error',
             'message': 'Нет возможности проверить время заката!'}
        )
    sunset_today = data['results']['sunset']
    today = datetime.today()
    sunset_today = datetime.strptime(sunset_today, '%I:%M:%S %p')
    sunset_today = sunset_today.replace(
        year=today.year, month=today.month, day=today.day
    )
    return sunset_today

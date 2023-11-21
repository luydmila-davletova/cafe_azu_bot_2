from django.core.exceptions import ValidationError

from reservation.models import Reservation


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

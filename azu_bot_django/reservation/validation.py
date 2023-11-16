from django.core.exceptions import ValidationError
from reservation.models import Reservation


def tables_in_cafe(reservation_data):
    tables_pk = reservation_data['table']
    for table in tables_pk:
        if reservation_data['cafe'].id != table.cafe.id:
            raise ValidationError(
                "Кафе и столы в кафе должны совпадать по местоположению"
            )


def tables_in_cafe_in_date(reservation_data):
    tables_pk = reservation_data['table']
    for table in tables_pk:
        if Reservation.objects.filter(
            cafe=reservation_data['cafe'],
            table=table,
            status='booked',
        ):
            raise ValidationError(
                "Активная бронь с этим столом на эту дату существует"
            )

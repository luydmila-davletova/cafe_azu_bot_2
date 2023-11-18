from django.db import models

from azu_bot_django.settings import MAX_CHAR_LENGTH
from cafe.models import Cafe
from menu.models import Set


class Reservation(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='В кафе'
    )
    date = models.DateField(
        'Дата бронирования'
    )
    name = models.CharField(
        'Имя клиента',
        max_length=MAX_CHAR_LENGTH
    )
    number = models.CharField(
        'Номер телефона клиента',
        max_length=MAX_CHAR_LENGTH
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('booked', 'Забронировано'),
            ('cancelled', 'Отменено')
        ],
        default=None
    )
    sets_and_quantities = models.ManyToManyField(
        'OrderSets',
        related_name='reservations'
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        ordering = ('date',)

    def __str__(self):
        return f'В кафе {self.cafe}, для {self.name} на {self.date}'


class OrderSets(models.Model):
    reservation = models.ForeignKey(
        'reservation.Reservation',
        on_delete=models.CASCADE,
        related_name='order_sets',
        default=None
    )
    sets = models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        related_name='order_sets'
    )
    quantity = models.IntegerField(
        'Количество сета'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.sets} в количестве {self.quantity}'


class TableReservation(models.Model):
    table = models.ForeignKey(
        'tables.Table',
        on_delete=models.CASCADE,
        related_name='table_reservations',
        verbose_name='Забронированный стол'
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='table_reservations',
        verbose_name='Бронь'
    )
    quantity = models.IntegerField('Количество мест')

    class Meta:
        verbose_name = 'Бронь стола'
        verbose_name_plural = 'Брони столов'

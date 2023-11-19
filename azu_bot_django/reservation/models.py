from django.db import models
from django.db.models import UniqueConstraint

from azu_bot_django.settings import MAX_CHAR_LENGHT, MAX_DIGIT_LENGHT
from cafe.models import Cafe
from menu.models import Set
from tables.models import Table

STATUS_DICT = [
    ('booked', 'Забронировано'),
    ('cancelled', 'Отменено')
]


class Reservation(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Кафе',
    )
    table = models.ManyToManyField(
        Table,
        verbose_name='Столы'
    )
    sets = models.ManyToManyField(
        Set,
        through='OrderSets',
        verbose_name='Заказы'
    )
    date = models.DateField(
        verbose_name='Дата бронирования'
    )
    name = models.CharField(
        'Имя клиента',
        max_length=MAX_CHAR_LENGTH
    )
    number = models.CharField(
        'Номер телефона клиента',
        max_length=MAX_DIGIT_LENGHT
    )
    status = models.CharField(
        max_length=MAX_CHAR_LENGHT,
        choices=STATUS_DICT,
        verbose_name='Статус брони'
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
        return f'Бронь в кафе {self.cafe} для {self.name} на {self.date}'


class OrderSets(models.Model):
    reservation = models.ForeignKey(
        'reservation.Reservation',
        on_delete=models.CASCADE,
        verbose_name='Бронь'
        related_name='order_sets',
        default=None
    )
    sets = models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        related_name='order_sets'
    )
    quantity = models.PositiveIntegerField(
        'Количество сета'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        constraints = [
            UniqueConstraint(
                fields=('reservation', 'set'),
                name='unique_reservation_set'
            ),
        ]

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

from django.db import models
from django.db.models import UniqueConstraint

from azu_bot_django.settings import MAX_CHAR_LENGTH, MAX_DIGIT_LENGTH
from cafe.models import Cafe
from menu.models import Set
from tables.models import Table

STATUS_CHOICES = [
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
        max_length=MAX_DIGIT_LENGTH
    )
    status = models.CharField(
        'Статус брони',
        max_length=MAX_CHAR_LENGTH,
        choices=STATUS_CHOICES,
        default='booked'
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
        verbose_name='Бронь',
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
                fields=('reservation', 'sets'),
                name='unique_reservation_sets'
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

    class Meta:
        verbose_name = 'Бронь стола'
        verbose_name_plural = 'Брони столов'

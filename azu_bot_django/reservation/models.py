from django.db import models
from django.db.models import UniqueConstraint

from cafe.models import Cafe
from menu.models import Set
from tables.models import Table


class Reservation(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name='Кафе'
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
        max_length=100,
        verbose_name='Имя клиента'
    )
    number = models.CharField(
        max_length=15,
        verbose_name='Номер телефона клиента'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('booked', 'Забронировано'),
            ('cancelled', 'Отменено')],
        default=False
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        ordering = ('date',)

    def __str__(self):
        return f'Бронь в кафе {self.cafe} для {self.name} на {self.date}'


class OrderSets(models.Model):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='order_sets',
        verbose_name='Бронь'
    )
    set = models.ForeignKey(
        Set,
        on_delete=models.CASCADE,
        verbose_name='Сет'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество сета'
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
        return f'Заказ {self.set} в количестве {self.quantity}'

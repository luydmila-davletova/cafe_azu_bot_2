from django.db import models
from cafe.models import Cafe


class Table(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='Кафе'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Размер стола (количество мест)'
    )

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ("cafe", "quantity")

    def __str__(self):
        return f'Стол в {self.cafe} на {self.quantity} человек'


class ReservationTable(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name='Стол'
    )
    date = models.DateField(
        'Дата бронирования'
    )

    class Meta:
        verbose_name = 'Бронь стола'
        verbose_name_plural = 'Брони стола'

    def __str__(self):
        return f'{self.table} занят на {self.date}'

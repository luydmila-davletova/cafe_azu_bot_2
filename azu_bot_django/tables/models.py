from django.db import models

from azu_bot_django.settings import MAX_CHAR_LENGTH
from cafe.models import Cafe

TABLE_TYPE_CHOICES = [
    ('simple_table', 'Обычный стол'),
    ('bar_table', 'Барный стол')]


class Table(models.Model):
    TABLE_TYPE_CHOICES = [
        ('simple_table', 'Простой стол'),
        ('bar_table', 'Барный стол')
    ]
    name = models.CharField(
        'Имя стола',
        max_length=MAX_CHAR_LENGTH,
        default=None
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='В кафе'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Размер стола (количество мест)'
    )
    table_type = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        choices=TABLE_TYPE_CHOICES,
        verbose_name='Тип стола',
        default=TABLE_TYPE_CHOICES[0][0]
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
        return f'Место в {self.cafe} - {self.quantity} человек'

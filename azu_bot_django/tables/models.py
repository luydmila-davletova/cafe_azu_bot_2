from django.db import models

from azu_bot_django.settings import MAX_CHAR_LENGHT
from cafe.models import Cafe

TABLE_TYPE_CHOICES = [
    ('simple_table', 'Обычный стол'),
    ('bar_table', 'Барный стол')]


class Table(models.Model):
    name = models.CharField(
        'Имя стола',
        max_length=MAX_CHAR_LENGHT,
        default=None
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='Кафе'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Размер стола (количество мест)'
    )
    table_type = models.CharField(
        max_length=MAX_CHAR_LENGHT,
        choices=TABLE_TYPE_CHOICES,
        verbose_name='Тип стола',
        default=None
    )

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ("cafe", "quantity")

    def __str__(self):
        return f'Стол в {self.cafe} на {self.quantity} человек'

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

from django.db import models
from cafe.models import Cafe


class Table(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='table_cafe',
        verbose_name='В кафе'
    )
    quantity = models.IntegerField(
        'Размер стола'
    )

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ("cafe", "quantity",)

    def __str__(self):
        return f'Cтол на в {self.cafe} размером {self.quantity} человек'

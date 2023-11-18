from django.db import models
from cafe.models import Cafe
from reservation.models import Reservation


class Table(models.Model):
    TABLE_TYPE_CHOICES = [
        ('simple_table', 'Простой стол'),
        ('bar_table', 'Барный стол')
    ]
    name = models.CharField('Имя стола', max_length=12, default=None)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE,
                             related_name='tables', verbose_name='В кафе')
    quantity = models.IntegerField('Размер стола')
    table_type = models.CharField(
        max_length=12,
        choices=TABLE_TYPE_CHOICES,
        verbose_name='Тип стола',
        default=TABLE_TYPE_CHOICES[0][0]
    )
    reservations = models.ManyToManyField(
        Reservation,
        blank=True,
        related_name='tables_reservations',
        verbose_name='Забронированные столы'
    )

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ("cafe", "quantity",)

    def __str__(self):
        return f'Место в {self.cafe} - {self.quantity} человек'

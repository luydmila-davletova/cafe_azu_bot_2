from django.db import models

from cafe.models import Cafe
from reservation.models import Reservation


class Table(models.Model):
    name = models.CharField(
        'Имя стола',
        max_length=12,
        default=None
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name='В кафе'
    )
    quantity = models.IntegerField(
        'Размер стола'
    )
    TABLE_TYPE_CHOICES = [
        ('simple_table', 'Место за столом'),
        ('bar_table', 'Барное место')]
    table_type = models.CharField(
        max_length=12,
        choices=TABLE_TYPE_CHOICES,
        verbose_name='Тип стола',
        default=None
    )
    reservations = models.ManyToManyField(
        'reservation.Reservation',
        blank=True,
        related_name='table_reservations',
        verbose_name='Забронированные столы'
    )

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'
        ordering = ("cafe", "quantity",)

    def __str__(self):
        return f'Cтол на в {self.cafe} размером {self.quantity} человек'


class SimpleTable(models.Model):
    name = models.CharField(
        'Имя стола',
        max_length=12,
        default=None
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='simple_tables',
        verbose_name='В кафе'
    )
    quantity = models.IntegerField(
        'Размер стола'
    )
    reservations = models.ManyToManyField(
        Reservation,
        blank=True,
        related_name='simple_table_reservations',
        verbose_name='Забронированные столы'
    )

    class Meta:
        verbose_name = 'Простой стол'
        verbose_name_plural = 'Простые столы'
        ordering = ("cafe", "quantity",)

    def __str__(self):
        return f'Стол {self.cafe} - {self.quantity} человек'


class BarTable(models.Model):
    name = models.CharField(
        'Имя барного места',
        max_length=12,
        default=None
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='bar_tables',
        verbose_name='В кафе'
    )
    quantity = models.IntegerField(
        'Размер стола'
    )
    reservations = models.ManyToManyField(
        'reservation.Reservation',
        blank=True,
        related_name='bar_table_reservations',
        verbose_name='Забронированные столы'
    )

    class Meta:
        verbose_name = 'Барный стол'
        verbose_name_plural = 'Барные столы'
        ordering = ("cafe", "quantity",)

    def __str__(self):
        return f'Bar {self.cafe} - {self.quantity} человек'

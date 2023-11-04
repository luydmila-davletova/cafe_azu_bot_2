from django.db import models
from cafe.models import Cafe
from menu.models import Set
from tables.models import Table


class Reservation(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='res_cafe',
        verbose_name='В кафе'
    )
    tables = models.ManyToManyField(
        Table,
        related_name='tables'
    )
    sets = models.ManyToManyField(
        "OrderSets"
    )
    date = models.DateField(
        'Дата бронирования'
    )
    name = models.CharField(
        'Имя клиента'
    )
    number = models.CharField(
        'Номер телефона клиента'
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        ordering = ("date",)

    def __str__(self):
        return f'В кафе {self.cafe}, для {self.name} на {self.date}'


class OrderSets(models.Model):
    sets = models.ForeignKey(Set, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        'Количество сета'
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.sets} в количестве {self.quantity}'

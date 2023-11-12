from django.contrib import admin
from django.db import models
from django.db.models import UniqueConstraint

from django.utils.html import format_html

#from ..azu_bot_django.settings import MAX_CHAR_LENGHT


class Dish(models.Model):
    name = models.CharField(
        'Название блюда',
        max_length=256
    )
    description = models.CharField(
        'Описание блюда',
        max_length=256
    )
    image = models.ImageField(
        upload_to='dishes/',
        verbose_name='Изображение блюда',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Set(models.Model):
    name = models.CharField(
        'Название сета',
        max_length=256,
        unique=True
    )
    description = models.CharField(
        'Описание сета',
        max_length=256
    )
    dishes = models.ManyToManyField(
        Dish,
        through='SetDish',
        verbose_name='Блюда',
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена сета'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество сетов'
    )

    image = models.ImageField(
        upload_to='sets/',
        verbose_name='Изображение сета',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Сет'
        verbose_name_plural = 'Сеты'
        ordering = ("price", "name",)

    def __str__(self):
        return f'{self.name} по цене {self.price}'


class SetDish(models.Model):
    """
    Связующий класс между Сетами(Set) и блюдами(Dish)
    """
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name='Количество блюд в сете')

    class Meta:
        verbose_name = 'Блюд в сете'
        verbose_name_plural = 'Блюд в сете'
        constraints = [
            UniqueConstraint(
                fields=('set', 'dish'),
                name='unique_set_dish'
            ),
        ]

    def __str__(self):
        return f'{self.quantity} {self.dish.name}'

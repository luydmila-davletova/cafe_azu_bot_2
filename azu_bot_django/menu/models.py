from django.contrib import admin
from django.db import models

from django.utils.html import format_html


class Dish(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название блюда'
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


class SetDish(models.Model):
    set = models.ForeignKey('Set', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество блюд')

    def __str__(self):
        return f'{self.quantity} {self.dish.name}'


class Set(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название сета'
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание сета'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена сета'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество сетов'
    )
    dishes = models.ManyToManyField(Dish, through=SetDish, verbose_name='Блюда', blank=True)
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

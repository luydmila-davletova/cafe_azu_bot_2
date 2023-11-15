from django.db import models

from azu_bot_django.settings import MAX_CHAR_LENGHT


class Set(models.Model):
    name = models.CharField(
        'Название сета',
        max_length=MAX_CHAR_LENGHT
    )
    description = models.CharField(
        'Описание сета',
        max_length=MAX_CHAR_LENGHT
    )
    dishes = models.ManyToManyField(
        'Dishes'
    )
    price = models.IntegerField(
        'Цена сета'
    )

    class Meta:
        verbose_name = 'Сет'
        verbose_name_plural = 'Сеты'
        ordering = ("price", "name",)

    def __str__(self):
        return f'Сет {self.name} по цене {self.price}'


class Dishes(models.Model):
    name = models.CharField(
        'Название блюда',
        max_length=MAX_CHAR_LENGHT
    )
    description = models.CharField(
        'Описание блюда',
        max_length=MAX_CHAR_LENGHT
    )

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ("name",)

    def __str__(self):
        return f'Блюдо {self.name}'

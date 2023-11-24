from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

from azu_bot_django.settings import (MAX_CHAR_LENGTH, MAX_DECIMAL_LENGTH,
                                     MAX_DIGIT_LENGTH)


class Dishes(models.Model):
    name = models.CharField(
        'Название блюда',
        max_length=MAX_CHAR_LENGTH
    )
    description = models.CharField(
        'Описание блюда',
        max_length=MAX_CHAR_LENGTH
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
        max_length=MAX_CHAR_LENGTH,
        unique=True
    )
    description = models.CharField(
        'Описание сета',
        max_length=MAX_CHAR_LENGTH
    )
    dishes = models.ManyToManyField(
        Dishes,
        through='SetDish',
        verbose_name='Блюда',
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Цена сета',
        decimal_places=MAX_DECIMAL_LENGTH,
        max_digits=MAX_DIGIT_LENGTH
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
        ordering = ('price', 'name',)

    def __str__(self):
        return f'{self.name} по цене {self.price}'


class SetDish(models.Model):
    """
    Связующий класс между Сетами(Set) и блюдами(Dish)
    """
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name='Количество блюд в сете',
        default=1
    )

    class Meta:
        verbose_name = 'Блюд в сете'
        verbose_name_plural = 'Блюд в сете'
        constraints = [
            UniqueConstraint(
                fields=('set', 'dish', 'quantity'),
                name='unique_set_dish_quantity'
            ),
        ]

    def clean(self):
        if SetDish.objects.filter(
            set=self.set,
            dish=self.dish,
            quantity=self.quantity
        ):
            raise ValidationError(
                'Такой сет уже существует!'
            )

    def __str__(self):
        return f'{self.quantity} {self.dish.name}'

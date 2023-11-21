from django.db import models
from django.db.models import UniqueConstraint

from azu_bot_django.settings import MAX_CHAR_LENGTH


class Cafe(models.Model):
    name = models.CharField(
        'Название кафе',
        max_length=MAX_CHAR_LENGTH,
        unique=True
    )
    address = models.CharField(
        'Адрес кафе',
        max_length=MAX_CHAR_LENGTH,
        unique=True
    )
    number = models.CharField(
        'Номер кафе',
        max_length=MAX_CHAR_LENGTH
    )

    class Meta:
        verbose_name = 'Кафе'
        verbose_name_plural = 'Кафе'
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=('name', 'address',),
                name='unique_name_address'
            ),
        ]

    def __str__(self):
        return f'{self.name} по адресу {self.address}'

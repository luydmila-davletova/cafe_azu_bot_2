from django.db import models

from azu_bot_django.settings import MAX_CHAR_LENGHT


class Cafe(models.Model):
    name = models.CharField(
        'Название кафе',
        max_length=MAX_CHAR_LENGHT
    )
    address = models.CharField(
        'Адрес кафе',
        max_length=MAX_CHAR_LENGHT
    )
    number = models.CharField(
        'Номер кафе',
        max_length=MAX_CHAR_LENGHT
    )

    class Meta:
        verbose_name = 'Кафе'
        verbose_name_plural = 'Кафе'
        ordering = ("name",)

    def __str__(self):
        return f'{self.name} по адресу {self.address}'

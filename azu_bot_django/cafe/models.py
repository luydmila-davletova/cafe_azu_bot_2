from django.db import models


class Cafe(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название кафе'
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Адрес кафе'
    )
    number = models.CharField(
        max_length=15,
        verbose_name='Номер кафе'
    )

    class Meta:
        verbose_name = 'Кафе'
        verbose_name_plural = 'Кафе'
        ordering = ("name",)

    def __str__(self):
        return f'{self.name} по адресу {self.address}'

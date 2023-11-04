from django.db import models


class Cafe(models.Model):
    name = models.CharField(
        'Название кафе'
    )
    address = models.CharField(
        'Адрес кафе'
    )
    number = models.CharField(
        'Номер кафе'
    )

    class Meta:
        verbose_name = 'Кафе'
        verbose_name_plural = 'Кафе'
        ordering = ("name",)

    def __str__(self):
        return f'{self.name} по адресу {self.address}'

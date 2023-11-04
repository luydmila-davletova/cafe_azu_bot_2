from django.db import models


class Set(models.Model):
    name = models.CharField(
        'Название сета'
    )
    description = models.CharField(
        'Описание сета'
    )
    price = models.IntegerField(
        'Цена сета'
    )

    class Meta:
        verbose_name = 'Сет'
        verbose_name_plural = 'Сеты'
        ordering = ("price", "name",)

    def __str__(self):
        return f'Кафе {self.name} по цене {self.price}'

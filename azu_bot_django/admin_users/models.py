from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.contenttypes.models import ContentType


from django.db import models
from cafe.models import Cafe
from reservation.models import OrderSets, Reservation


class CustomUser(AbstractUser):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        verbose_name='В кафе',
        blank=True,
        null=True,
        help_text="Для сотрудников кафе обязателен выбор к привязанному кафе",
    )
    is_cafe_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ("username",)

    def __str__(self):
        return self.username

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        """
        Автоматическое добавление прав доступа при создании
        """
        super().save(force_insert, force_update, *args, **kwargs)
        if self.is_cafe_admin:
            cafe_admin_group, created = Group.objects.get_or_create(
                name='Cafe Admin'
            )
            self.groups.add(cafe_admin_group)
            reservations_permissions = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(Reservation)
            )
            order_sets_permissions = Permission.objects.filter(
                content_type=ContentType.objects.get_for_model(OrderSets)
            )
            self.user_permissions.add(
                *reservations_permissions,
                *order_sets_permissions
            )

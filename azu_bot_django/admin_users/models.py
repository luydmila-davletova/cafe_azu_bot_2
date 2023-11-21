from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
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
        help_text='Для сотрудников кафе обязателен выбор к привязанному кафе',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    def clean(self):
        """Если пользователь админ - может заходить в админку"""
        if not self.cafe:
            raise ValidationError(
                'Выберите кафе к которому приписан администратор'
            )
        self.is_staff = True

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        """
        Автоматическое добавление прав доступа при создании
        """
        super().save(force_insert, force_update, *args, **kwargs)
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

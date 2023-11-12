from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType

from reservation.models import Reservation, OrderSets
from .models import Profile


@receiver(post_save, sender=Profile)
def add_permissions(sender, instance, **kwargs):
    if instance.is_cafe_admin:
        reservations_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Reservation)
        )
        order_sets_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(
                OrderSets
            )
        )

        instance.user.user_permissions.add(
            *reservations_permissions,
            *order_sets_permissions
        )

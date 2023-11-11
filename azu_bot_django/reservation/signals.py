# В файле signals.py вашего приложения reservation
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Permission, Group
from admin_users.models import Profile
from reservation.models import OrderSets, Reservation


@receiver(post_save, sender=Profile)
def create_cafe_admin(sender, instance, created, **kwargs):
    if created and instance.is_cafe_admin:
        user = User.objects.create_user(username=instance.user.username, password='default_password')
        cafe_admin_group, created = Group.objects.get_or_create(name='Cafe Admin')
        user.groups.add(cafe_admin_group)
        reservations_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Reservation)
        )
        order_sets_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(OrderSets)
        )
        user.user_permissions.add(*reservations_permissions, *order_sets_permissions)
        instance.user = user
        instance.save()

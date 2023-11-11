from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from reservation.models import OrderSets, Reservation
from .models import Profile
from cafe.models import Cafe


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


@receiver(post_save, sender=Profile)
def create_cafe_admin(sender, instance, created, **kwargs):
    if created and instance.is_cafe_admin:
        username = instance.user.username
        existing_user = User.objects.filter(username=username).first()

        if not existing_user:
            user = User.objects.create_user(username=username, password='default_password')
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


admin.site.unregister(Cafe)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Cafe)
admin.site.register(Profile)

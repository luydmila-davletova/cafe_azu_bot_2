from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from admin_users.models import CustomUser

ADD_CUSTOM_FIELDS_IN_USER_FORM = ((
    'Работает в кафе',
    {'fields': ('cafe',)}
),)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name',
                    'last_name', 'cafe')
    UserAdmin.fieldsets += ADD_CUSTOM_FIELDS_IN_USER_FORM
    UserAdmin.add_fieldsets += ADD_CUSTOM_FIELDS_IN_USER_FORM

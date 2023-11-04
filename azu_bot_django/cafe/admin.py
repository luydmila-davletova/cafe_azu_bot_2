from django.contrib import admin
from .models import Cafe


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "number")

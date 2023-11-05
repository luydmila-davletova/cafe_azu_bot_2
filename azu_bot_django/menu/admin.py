from django.contrib import admin
from .models import Set, SetDish, Dish


class SetDishInline(admin.TabularInline):
    model = SetDish
    extra = 1


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "price")
    inlines = [SetDishInline]


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from django.utils.html import format_html

from .models import Set, SetDish, Dish


class SetDishInline(admin.TabularInline):
    model = SetDish
    extra = 1


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    inlines = [SetDishInline]
    list_display = ("name", "description", "price", "quantity", "display_image")
    search_fields = ("name",)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="50" />'.format(obj.image.url))
        return None

    display_image.short_description = 'Изображение'


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    pass
  
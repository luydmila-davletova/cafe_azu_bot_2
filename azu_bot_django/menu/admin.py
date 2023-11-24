from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import Dishes, Set, SetDish


class SetDishInline(admin.TabularInline):
    model = SetDish
    extra = 1


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'description',
        'price'
    )
    search_fields = ('name',)
    inlines = [SetDishInline]

    def view_dishes(self, obj):
        count = obj.dishes.count()
        if count == 1:
            short_description = 'блюда'
        else:
            short_description = 'блюд'
        url = (
            reverse('admin:menu_dish_changelist')
            + '?'
            + urlencode({'set__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} {}</a>', url, count, short_description
        )

    view_dishes.short_description = 'Блюд'



@admin.register(Dishes)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode
from .models import Reservation, OrderSets


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("cafe", "view_tables", "view_order_sets",
                    "name", "number", "date")
    list_filter = ("date", )

    def view_tables(self, obj):
        count = obj.tables.count()
        if count == 1:
            short_description = 'Стол'
        elif 1 < count < 5:
            short_description = 'Стола'
        else:
            short_description = 'Столов'
        url = (
            reverse("admin:tables_table_changelist")
            + "?"
            + urlencode({"reservation__id": f"{obj.id}"})
        )
        return format_html(
            '<a href="{}">{} {}</a>', url, count, short_description
        )
    view_tables.short_description = 'Столов'

    def view_order_sets(self, obj):
        count = obj.sets.count()
        if count == 1:
            short_description = 'Заказ'
        elif 1 < count < 5:
            short_description = 'Заказа'
        else:
            short_description = 'Заказов'
        url = (
            reverse("admin:reservation_ordersets_changelist")
            + "?"
            + urlencode({"reservation__id": f"{obj.id}"})
        )
        return format_html(
            '<a href="{}">{} {}</a>', url, count, short_description
        )
    view_order_sets.short_description = "Сетов"


@admin.register(OrderSets)
class OrderSetsAdmin(admin.ModelAdmin):
    pass

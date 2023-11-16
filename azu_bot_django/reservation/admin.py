from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from cafe.models import Cafe
from tables.models import Table
from reservation.models import OrderSets, Reservation
from reservation.validation import (
    tables_in_cafe,
    tables_in_cafe_in_date
)


class OrderSetsInline(admin.TabularInline):
    model = OrderSets
    extra = 1


class ReservationForm(forms.ModelForm):

    def clean(self):
        """
        Проверка полей
        """
        super().clean()
        data = self.cleaned_data
        tables_in_cafe(data)
        tables_in_cafe_in_date(data)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("cafe", "view_tables", "view_order_sets",
                    "name", "number", "date")
    list_filter = ("date", "cafe")
    inlines = [OrderSetsInline]
    form = ReservationForm

    def get_form(self, request, obj=None, **kwargs):
        """
        Получение экземляров других моделей, приписанных пользователю
        при создании брони
        """
        form = super(ReservationAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        form.base_fields['cafe'].queryset = Cafe.objects.filter(
            pk=request.user.cafe.id)
        form.base_fields['table'].queryset = Table.objects.filter(
            cafe=request.user.cafe.id)
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                cafe=request.user.cafe
            )
        return queryset

    def view_tables(self, obj):
        """
        Отображение количества забронированых столов
        и их вместительности на панели броней
        """
        count = obj.table.count()
        quantity = ''
        if count == 1:
            short_description = ' Стол '
        elif 1 < count < 5:
            short_description = ' Стола '
        else:
            short_description = ' Столов '
        for table in obj.table.all():
            if quantity:
                quantity += ', '
            quantity += str(table.quantity)

        return str(count) + short_description + 'на ' + quantity + ' человек'
    view_tables.short_description = 'Столов'

    def view_order_sets(self, obj):
        """
        Отображение количества заказов
        и ссылка для перехода на них
        """
        count = obj.sets.count()
        if count == 1:
            short_description = 'Заказ'
        elif 1 < count < 5:
            short_description = 'Заказа'
        else:
            short_description = 'Заказов'

        url = reverse(
            "admin:reservation_order_sets_changelist",
            args=[obj.id]
        )
        if count > 0:
            url += f"?{urlencode({'reservation__id__exact': f'{obj.id}'})}"

        return format_html(
            '<a href="{}">{} {}</a>',
            url, count,
            short_description
        )
    view_order_sets.short_description = "Сетов"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:reservation_id>/order_sets/',
                self.admin_site.admin_view(self.order_sets_changelist),
                name='reservation_order_sets_changelist',
            ),
        ]
        return custom_urls + urls

    def order_sets_changelist(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, pk=reservation_id)

        if request.method == 'POST':
            set_id = request.POST.get('set_id')
            quantity = request.POST.get('quantity')
            OrderSets.objects.create(
                reservation=reservation,
                set_id=set_id,
                quantity=quantity
            )
            url = reverse(
                "admin:reservation_order_sets_changelist",
                args=[reservation_id]
            )
            return HttpResponseRedirect(url)

        context = {
            'reservation': reservation,
            'order_sets': reservation.order_sets.all(),
        }
        return render(
            request,
            'admin/reservation/ordersets/change_list.html',
            context
        )

    def delete_reservation(self, request, reservation_id):
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.delete()
        return HttpResponseRedirect(
            reverse("admin:reservation_reservation_changelist")
        )


@admin.register(OrderSets)
class OrderSetsAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        """
        Получение экземляров других моделей, приписанных пользователю
        при создании брони
        """
        form = super(OrderSetsAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_superuser:
            return form
        form.base_fields['reservation'].queryset = Reservation.objects.filter(
            cafe=request.user.cafe.id)
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                reservation__cafe__id=request.user.cafe.id
            )
        return queryset

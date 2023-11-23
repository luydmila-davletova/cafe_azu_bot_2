from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from cafe.models import Cafe
from reservation.models import OrderSets, Reservation
from reservation.validation import (tables_available, tables_in_cafe,
                                    tables_in_cafe_in_date)
from tables.models import Table

from .models import OrderSets, Reservation


class OrderSetsInline(admin.TabularInline):
    model = OrderSets
    extra = 1


class ReservationForm(forms.ModelForm):

    def clean(self):
        """
        Проверка полей
        """
        super().clean()
        if self.is_valid():
            tables_in_cafe(self)
            tables_in_cafe_in_date(self)
            tables_available(self)
        return self.cleaned_data


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('cafe', 'view_tables', 'view_order_sets',
                    'name', 'number', 'date')
    list_filter = ('date', 'status')
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
        Отображение количества заказанных сетов
        и переход на панель с этими заказами
        """
        count = obj.sets.count()
        if count == 1:
            short_description = 'Заказ'
        elif 1 < count < 5:
            short_description = 'Заказа'
        else:
            short_description = 'Заказов'
        url = (
            reverse('admin:reservation_ordersets_changelist')
            + '?'
            + urlencode({'reservations__id': f'{obj.id}'})
        )
        return format_html(
            '<a href="{}">{} {}</a>', url, count, short_description
        )
    view_order_sets.short_description = 'Сетов'


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

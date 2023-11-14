from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from reservation.models import OrderSets, Reservation


class OrderSetsInline(admin.TabularInline):
    model = OrderSets
    extra = 1


class ReservationForm(forms.ModelForm):
    def clean(self):
        """
        Проверка нахождения столов в забронированном кафе
        """
        super(ReservationForm, self).clean()
        tables_pk = self.cleaned_data['tables']
        for table in tables_pk:
            if self.cleaned_data['cafe'].id != table.table.cafe.id:
                raise ValidationError(
                    "Кафе и столы в кафе должны совпадать по местоположению")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("cafe", "view_tables", "view_order_sets",
                    "name", "number", "date")
    list_filter = ("date", "cafe")
    inlines = [OrderSetsInline]
    form = ReservationForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                cafe=request.user.profile.cafe
            )
        return queryset

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if obj.cafe != request.user.profile.cafe:
                raise ValidationError(
                    "Можно создать бронь только для своего кафе!")
        super().save_model(request, obj, form, change)

    def view_tables(self, obj):
        """
        Отображение количества забронированых столов
        и их вместительности на панели броней
        """
        count = obj.tables.count()
        quantity = ''
        if count == 1:
            short_description = ' Стол '
        elif 1 < count < 5:
            short_description = ' Стола '
        else:
            short_description = ' Столов '
        for table in obj.tables.all():
            if quantity:
                quantity += ', '
            quantity += str(table.table.quantity)

        return str(count) + short_description + 'на ' + quantity + ' человек'
    view_tables.short_description = 'Столов'

    def view_order_sets(self, obj):
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
    pass

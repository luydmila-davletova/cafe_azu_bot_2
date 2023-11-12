from django.contrib import admin

from tables.models import Table, ReservationTable


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("cafe", "quantity")

    def get_queryset(self, request):
        """
        Персонал получит информацию о столах в его кафе,
        суперпользователя это не касается
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(cafe=request.user.cafe.id)


@admin.register(ReservationTable)
class ReservationTableAdmin(admin.ModelAdmin):
    list_display = ("table", "date")

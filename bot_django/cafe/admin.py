from django.contrib import admin

from .models import Cafe


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'number')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(
                cafe=request.user.cafe
            )
        return queryset

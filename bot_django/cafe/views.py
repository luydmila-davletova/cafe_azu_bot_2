from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import JsonResponse
from datetime import date

from cafe.models import Cafe
from tables.models import Table
from reservation.models import Reservation
from cafe.serializers import CafeSerializer
from admin_users.models import CustomUser


class CafeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

    @action(methods=['POST'], detail=True)
    def quantity(self, request, pk):
        data = request.data
        if 'quantity' not in data.keys():
            return JsonResponse({
                'date': [
                    'Обязательное поле.'
                ]
            })
        cafe = Cafe.objects.get(id=pk)
        res_date = date.fromisoformat(data['date'])
        available_tables = Table.objects.filter(
            cafe=cafe).exclude(
            id__in=Reservation.table.through.objects.filter(
                reservation__cafe__id=cafe.id,
                reservation__date=res_date,
                reservation__status='booked'
            ).values('table')
        )
        quantity = 0
        for table in available_tables:
            quantity += table.quantity
        return JsonResponse({
            'cafe': cafe.address,
            'date': res_date,
            'quantity': quantity
        })

    @action(methods=['GET'], detail=True)
    def admins(self, request, pk):
        cafe = Cafe.objects.get(id=pk)
        cafe_admins = CustomUser.objects.filter(cafe=cafe)
        answer = []
        for admin in cafe_admins:
            answer.append({
                'name': admin.first_name,
                'telegram': admin.telegram_id
            })
        return JsonResponse(
            {'cafe': cafe.address,
             'admins': answer}
        )

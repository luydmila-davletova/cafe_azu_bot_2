from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from cafe.models import Cafe
from reservation.models import Reservation
from reservation.serializers import (ReservationReadSerializer,
                                     ReservationWriteSerializer)
from reservation.validation import cancell_reservation


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()

    def get_cafe(self):
        cafe_id = self.kwargs.get('cafe_id')
        return get_object_or_404(Cafe, id=cafe_id)

    def get_queryset(self):
        return Reservation.objects.filter(cafe=self.get_cafe())

    def get_serializer_class(self):
        method = self.request.method
        if method in ('PATCH', 'GET'):
            return ReservationReadSerializer
        return ReservationWriteSerializer

    def perform_create(self, serializer):
        cafe = self.get_cafe()
        return serializer.save(cafe=cafe)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = ReservationReadSerializer(instance)
        return Response(instance_serializer.data)

    def perform_update(self, serializer):
        cancell_reservation(serializer)

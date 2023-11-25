from rest_framework import viewsets
from rest_framework.response import Response

from menu.models import Dishes, Set
from menu.serializers import (DishesSerializer, SetReadSerializer,
                              SetWriteSerializer)


class DishesViewSet(viewsets.ModelViewSet):
    queryset = Dishes.objects.all()
    serializer_class = DishesSerializer


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return SetReadSerializer
        return SetWriteSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = SetReadSerializer(instance)
        return Response(instance_serializer.data)

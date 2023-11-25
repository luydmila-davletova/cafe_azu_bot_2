from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from cafe.models import Cafe
from tables.models import Table
from tables.serializers import TableSerializer
from asgiref.sync import sync_to_async


class TableViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    @sync_to_async
    def get_cafe(self):
        cafe_id = self.kwargs.get('cafe_id')
        return get_object_or_404(Cafe, id=cafe_id)

    @sync_to_async
    def get_queryset(self):
        return Table.objects.filter(cafe=self.get_cafe())

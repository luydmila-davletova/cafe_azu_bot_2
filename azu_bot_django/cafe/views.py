from rest_framework import viewsets

from cafe.models import Cafe
from cafe.serializers import CafeSerializer


class CafeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer

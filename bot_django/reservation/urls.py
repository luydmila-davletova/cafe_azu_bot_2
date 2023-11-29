from django.urls import include, path
from rest_framework.routers import SimpleRouter

from reservation.views import ReservationViewSet

app_name = 'reservation'

router_v1 = SimpleRouter()
router_v1.register('', ReservationViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]

from django.urls import include, path
from rest_framework.routers import SimpleRouter

from cafe.views import CafeViewSet

app_name = 'cafe'

router_v1 = SimpleRouter()
router_v1.register('', CafeViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]

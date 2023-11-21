from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tables.views import TableViewSet

app_name = 'tables'

router_v1 = SimpleRouter()
router_v1.register('', TableViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]

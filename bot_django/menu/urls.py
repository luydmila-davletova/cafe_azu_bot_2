from django.urls import include, path
from rest_framework.routers import SimpleRouter

from menu.views import DishesViewSet, SetViewSet

app_name = 'menu'

router_v1 = SimpleRouter()
router_v1.register('dishes', DishesViewSet)
router_v1.register('sets', SetViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]

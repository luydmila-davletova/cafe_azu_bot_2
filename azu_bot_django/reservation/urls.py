from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'create_location/',
        views.create_location,
        name='create_location'
    ),
    path(
        'update_location/<int:location_id>/',
        views.update_location,
        name='update_location'
    ),
    path(
        'delete_location/<int:location_id>/',
        views.delete_location,
        name='delete_location'
    ),
    path('book_table/', views.book_table, name='book_table'),
    path('create_combo/', views.create_combo, name='create_combo'),
    path('create_dish/', views.create_dish, name='create_dish'),
]

"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_sede, name='create_sede'),
    path('listing', views.listing_sede, name='listing_sede'),
    path('update/<int:sede_id>', views.form_sede, name='update_sede'),
    path('add', webservices.add_sede, name='add_sede'),
    path('replace/<int:sede_id>', webservices.replace_sede, name='replace_sede'),
    path('picker_search', webservices.picker_search_sede, name='picker_search_sede'),
    path('data_list', webservices.list_sede, name='data_list_sede'),
    path('get/<int:sede_id>', webservices.get_sede, name='get_sede'),
    path('delete/<int:sede_id>', webservices.delete_sede, name='delete_sede'),
    path('toggle/<int:sede_id>', webservices.toggle_sede, name='toggle_sede'),
    path('picker_search_bodega', webservices.picker_search_bodega, name='picker_search_bodega'),
    path('get_bodega/<int:bodega_id>', webservices.get_bodega, name='get_bodega'),
]

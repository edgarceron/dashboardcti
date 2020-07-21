"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_asesor, name='create_asesor'),
    path('listing', views.listing_asesor, name='listing_asesor'),
    path('update/<int:asesor_id>', views.form_asesor, name='update_asesor'),
    path('add', webservices.add_asesor, name='add_asesor'),
    path('replace/<int:asesor_id>', webservices.replace_asesor, name='replace_asesor'),
    path('picker_search', webservices.picker_search_asesor, name='picker_search_asesor'),
    path('data_list', webservices.list_asesor, name='data_list_asesor'),
    path('get/<int:asesor_id>', webservices.get_asesor, name='get_asesor'),
    path('delete/<int:asesor_id>', webservices.delete_asesor, name='delete_asesor'),
    path('toggle/<int:asesor_id>', webservices.toggle_asesor, name='toggle_asesor'),
]

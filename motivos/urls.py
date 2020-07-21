"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_motivo, name='create_motivo'),
    path('listing', views.listing_motivo, name='listing_motivo'),
    path('update/<int:motivo_id>', views.form_motivo, name='update_motivo'),
    path('add', webservices.add_motivo, name='add_motivo'),
    path('replace/<int:motivo_id>', webservices.replace_motivo, name='replace_motivo'),
    path('picker_search', webservices.picker_search_motivo, name='picker_search_motivo'),
    path('data_list', webservices.list_motivo, name='data_list_motivo'),
    path('get/<int:motivo_id>', webservices.get_motivo, name='get_motivo'),
    path('delete/<int:motivo_id>', webservices.delete_motivo, name='delete_motivo'),
    path('toggle/<int:motivo_id>', webservices.toggle_motivo, name='toggle_motivo'),
]

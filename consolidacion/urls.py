"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_consolidacion, name='create_consolidacion'),
    path('listing', views.listing_consolidacion, name='listing_consolidacion'),
    path(
        'upload_consolidacion_form', 
        views.upload_consolidacion_form, 
        name='upload_consolidacion_form'
    ),
    path('update/<int:consolidacion_id>', views.form_consolidacion, name='update_consolidacion'),
    path('add', webservices.add_consolidacion, name='add_consolidacion'),
    path('replace/<int:consolidacion_id>', webservices.replace_consolidacion, name='replace_consolidacion'),
    path('picker_search', webservices.picker_search_consolidacion, name='picker_search_consolidacion'),
    path('data_list', webservices.list_consolidacion, name='data_list_consolidacion'),
    path('get/<int:consolidacion_id>', webservices.get_consolidacion, name='get_consolidacion'),
    path('delete/<int:consolidacion_id>', webservices.delete_consolidacion, name='delete_consolidacion'),
    path('toggle/<int:consolidacion_id>', webservices.toggle_consolidacion, name='toggle_consolidacion'),
    path('upload_consolidacion', webservices.upload_consolidacion, name='upload_consolidacion'),
]

"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_consolidacion, name='create_consolidacion'),
    path('listing', views.listing_consolidacion, name='listing_consolidacion'),
    path(
        'download_consolidaciones/<int:agent>/<str:start_date>/<str:end_date>/<int:date_type>/<int:sede>/<str:estado>',
        views.download_consolidaciones,
        name='download_consolidaciones'
    ),
    path(
        'download_fails/<str:start_date>/<str:end_date>',
        views.download_fails,
        name='download_fails'
    ),
    path(
        'upload_consolidacion_form', 
        views.upload_consolidacion_form, 
        name='upload_consolidacion_form'
    ),
    path(
        'datos_consolidacion', 
        views.datos_consolidacion, 
        name='datos_consolidacion'
    ),
    path('turnero/<int:sede_id>', views.turnero, name='turnero'),
    path('update/<int:consolidacion_id>', views.form_consolidacion, name='update_consolidacion'),
    path('add', webservices.add_consolidacion, name='add_consolidacion'),
    path('replace/<int:consolidacion_id>', webservices.replace_consolidacion, name='replace_consolidacion'),
    path('picker_search', webservices.picker_search_consolidacion, name='picker_search_consolidacion'),
    path('data_list', webservices.list_consolidacion, name='data_list_consolidacion'),
    path('get/<int:consolidacion_id>', webservices.get_consolidacion, name='get_consolidacion'),
    path('delete/<int:consolidacion_id>', webservices.delete_consolidacion, name='delete_consolidacion'),
    path('toggle/<int:consolidacion_id>', webservices.toggle_consolidacion, name='toggle_consolidacion'),
    path('upload_consolidacion', webservices.upload_consolidacion, name='upload_consolidacion'),
    path('validate_cedula', webservices.validate_cedula, name='validate_cedula'),
    path('check_tercero_cedula', webservices.check_tercero_cedula, name='check_tercero_cedula'),
    path('check_placa', webservices.check_placa, name='check_placa'),
    path('get_closest_turns', webservices.get_closest_turns, name='get_closest_turns'),
    path('fail_prepare', webservices.fail_prepare, name='fail_prepare'),
    path('listing_citas_taller', webservices.listing_citas_taller, name='listing_citas_taller'),
    path('cancel_cita', webservices.cancel_cita, name='cancel_cita'),
]

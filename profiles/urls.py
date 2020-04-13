"""Urls for users app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form, name='create_profile'),
    path('listing', views.listing, name='listing_profile'),
    path('update/<int:profile_id>', views.form, name='update_profile'),
    path('add', webservices.add_profile, name='add_profile'),
    path('replace/<int:profile_id>', webservices.replace_profile, name='replace_profile'),
    path('picker_list', webservices.picker_search_profile, name='picker_list_profile'),
    path('data_list', webservices.list_profile, name='data_list_profile'),
    path('get/<int:profile_id>', webservices.get_profile, name='get_profile'),
    path('delete/<int:profile_id>', webservices.delete_profile, name='delete_profile'),
    path('toggle/<int:profile_id>', webservices.toggle_profile, name='toggle_profile'),
]
"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_campaign, name='create_campaign'),
    path('listing', views.listing_campaign, name='listing_campaign'),
    path('update/<int:campaign_id>', views.form_campaign, name='update_campaign'),
    path('upload_data_campaign/<int:campaign_id>', views.upload_data_campaign, name='upload_data_campaign'),
    path('add', webservices.add_campaign, name='add_campaign'),
    path('replace/<int:campaign_id>', webservices.replace_campaign, name='replace_campaign'),
    path('picker_search', webservices.picker_search_campaign, name='picker_search_campaign_manticore'),
    path('data_list', webservices.list_campaign, name='data_list_campaign'),
    path('get/<int:campaign_id>', webservices.get_campaign, name='get_campaign_manticore'),
    path('delete/<int:campaign_id>', webservices.delete_campaign, name='delete_campaign'),
    path('toggle/<int:campaign_id>', webservices.toggle_campaign, name='toggle_campaign'),
    path('upload_calls_campaign', webservices.upload_calls_campaign, name='upload_calls_campaign'),
]

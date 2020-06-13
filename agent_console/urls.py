"""Urls for agent_console app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_user_agent, name='create_user_agent'),
    path('update/<int:user_id>', views.form_user_agent, name='update_user_agent'),
    path('set_user_agent', webservices.set_user_agent, name='set_user_agent'),
    path('get_agent/<int:user_id>', webservices.get_agent, name='get_agent'),
    path('picker_search_agent', webservices.picker_search_agent, name='picker_search_agent')
]

"""Urls for dashboard app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard_dashboard'),
    path('dashboard_options_form', views.dashboard_options_form, name='dashboard_options_form'),
    path(
        'get_options_dashboard',
        webservices.get_options_dashboard,
        name='get_options_dashboard'
    ),
    path(
        'replace_options_dashboard',
        webservices.replace_options_dashboard,
        name='replace_options_dashboard'
    ),
    path(
        'get_data_dashboard',
        webservices.get_data_dashboard,
        name='get_data_dashboard'
    ),
]

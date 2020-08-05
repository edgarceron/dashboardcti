"""Urls for dashboard app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard_dashboard'),
]
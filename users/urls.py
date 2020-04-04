from django.urls import path

from . import views
from . import webservices

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.form, name='create'),
    path('listing', views.listing, name='listing'),
    path('update/<int:id>', views.form, name='update'),
    path('add', webservices.add_user, name='add'),
    path('picker_list', webservices.picker_search_user, name='picker_list'),
    path('data_list', webservices.list_user, name='data_list')
]
from django.urls import path

from . import views
from . import webservices

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.form, name='create'),
    path('update/<int:id>', views.form, name='update'),

    path('add', webservices.add_user, name='add'),

]
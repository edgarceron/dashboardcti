"""Contains the urls for the form_creator app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_form, name='create_form'),
    path('listing', views.listing_form, name='listing_form'),
    path('update/<int:form_id>', views.form_form, name='update_form'),
    path('add', webservices.add_form, name='add_form'),
    path('replace/<int:form_id>', webservices.replace_form, name='replace_form'),
    path('picker_search', webservices.picker_search_form, name='picker_search_form'),
    path('data_list', webservices.list_form, name='data_list_form'),
    path('get/<int:form_id>', webservices.get_form, name='get_form'),
    path('delete/<int:form_id>', webservices.delete_form, name='delete_form'),
    path('toggle/<int:form_id>', webservices.toggle_form, name='toggle_form'),
    path('add_question', webservices.add_question, name='add_question'),
    path('replace_question', webservices.replace_question, name='replace_question'),
    path('delete_question', webservices.delete_question, name='delete_question'),
    path(
        'change_question_position',
        webservices.change_question_position,
        name='change_question_position'
    )
]

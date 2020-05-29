""" Contains the views for the maingui module"""
import datetime
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    """ Returns the render for the index page"""
    return render(
        request,
        'maingui/index.html',
        {
            'username': "Invitado"
        }
    )

def login(request):
    """ Returns the render for the login page"""
    now = datetime.datetime.now()
    return render(
        request,
        'maingui/login.html',
        {
            'year': str(now.year)
        }
    )

""" Contains the views for the maingui module"""
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.permission_validation import PermissionValidation

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
    permission_obj = PermissionValidation(request)
    if permission_obj.login_session is None:
        now = datetime.datetime.now()
        return render(
            request,
            'maingui/login.html',
            {
                'year': str(now.year)
            }
        )
    return redirect('index')

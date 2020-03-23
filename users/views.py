from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Profile

def index(request):
    #TODO verificar usuario y permisos
    return render(
        request,
        'users/index.html',
        {
            'username': "Mauricio"
        }
    )

def form(request, id = 0):
    if(id == 0):
        action = "Crear"
    else:
        action = "Actualizar"
    #TODO verificar usuario y permisos

    return render(
        request,
        'users/form.html',
        {
            'id':id,
            'action':action,
            'username': "Mauricio"
        }
    )
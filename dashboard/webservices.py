"""Contains the webservices for the maingui app"""
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from agent_console.models import CurrentCallEntry

# Create your views here.
def get_actions():
    actions = [
       #{"name": "index", "label": "Pagina principal del modulo de usuario"},
    ]
    return actions

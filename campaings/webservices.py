"""Contains the webservices for the form_creator app"""
import datetime
import pytz
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.permission_validation import PermissionValidation

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_campaign", "label": "Webservice crear campaña"},
        {"name": "replace_campaign", "label": "Webservice actualizar campaña"},
        {"name": "get_campaign", "label": "Webservice obtener datos campaña"},
        {"name": "delete_campaign", "label": "Webservice borrar campaña"},
        {"name": "picker_search_campaign", "label": "Webservice picker de campañas"},
        {"name": "list_campaign", "label": "Webservice del listado de campañas"},
    ]
    return actions

@api_view(['POST'])
def add_campaign(request):
    pass

@api_view(['PUT'])
def replace_campaign(request, campaign_id):
    pass

@api_view(['POST'])
def get_campaign(request, campaign_id):
    pass

@api_view(['DELETE'])
def delete_campaign(request, campaign_id):
    pass

@api_view(['POST'])
def toggle_campaign(request, campaign_id):
    pass

@api_view(['POST'])
def picker_search_campaign(request):
    pass

@api_view(['POST'])
def list_campaign(request):
    pass 
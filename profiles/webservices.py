"""Contains the webservices for the profiles app"""
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.crud.standard import Crud
from users.permission_validation import PermissionValidation
from profiles.business_logic import profile_management, data_filters
from .serializers import ProfileSerializer, ProfilePermissionsSerializer
from .models import Profile, ProfilePermissions


def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_profile", "label": "Webservice crear perfil"},
        {"name": "replace_profile", "label": "Webservice actualizar perfil"},
        {"name": "get_profile", "label": "Webservice obtener datos perfil"},
        {"name": "delete_profile", "label": "Webservice borrar perfil"},
        {"name": "picker_search_profile", "label": "Webservice picker de perfiles"},
        {"name": "list_profile", "label": "Webservice del listado de perfiles"},
        {"name": "toggle_profile", "label": "Webservice para cambiar estado del perfil"},
    ]
    return actions

@api_view(['POST'])
def add_profile(request):
    """Tries to create an profile and returns the result"""
    crud_object = Crud(ProfileSerializer, Profile, None, profile_management.manage_profile_actions)
    return crud_object.add(request, 'add_profile')

@api_view(['PUT'])
def replace_profile(request, profile_id):
    """Tries to update an user and returns the result"""
    crud_object = Crud(ProfileSerializer, Profile, None, profile_management.manage_profile_actions)
    return crud_object.replace(request, profile_id, 'replace_profile')

@api_view(['POST'])
def get_profile(request, profile_id):
    """Return a JSON response with profile data for the given id"""
    crud_object = Crud(ProfileSerializer, Profile, None, profile_management.concat_profile_actions)
    return crud_object.get(request, profile_id, 'get_profile')

@api_view(['DELETE'])
def delete_profile(request, profile_id):
    """Tries to delete an profile and returns the result."""
    crud_object = Crud(ProfileSerializer, Profile)
    return crud_object.delete(request, profile_id, 'delete_profile', "Perfil elminado exitosamente")

@api_view(['POST'])
def toggle_profile(request, profile_id):
    """Toogles the active state for a given profile"""
    crud_object = Crud(ProfileSerializer, Profile)
    return crud_object.toggle(request, profile_id, 'toggle_profile', "Perfil")

@api_view(['POST'])
def picker_search_profile(request):
    """Returns a JSON response with profile data for a selectpicker."""
    crud_object = Crud(ProfileSerializer, Profile, data_filters.profile_picker_filter)
    return crud_object.picker_search(request, 'picker_search_profile')

@api_view(['POST'])
def list_profile(request):
    """ Returns a JSON response containing registered users"""
    crud_object = Crud(ProfileSerializer, Profile, data_filters.profiles_listing_filter)
    return crud_object.listing(request, 'list_profile')

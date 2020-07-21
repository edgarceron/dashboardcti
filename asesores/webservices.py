"""Contains the webservices for the asesores app"""
from rest_framework.decorators import api_view
from rest_framework import status
from core.crud.standard import Crud
from asesores.business_logic import data_filters
from .models import Asesor
from .serializers import AsesorSerializer

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_asesor", "label": "Webservice crear asesor"},
        {"name": "replace_asesor", "label": "Webservice actualizar asesor"},
        {"name": "get_asesor", "label": "Webservice obtener datos asesor"},
        {"name": "delete_asesor", "label": "Webservice borrar asesor"},
        {"name": "picker_search_asesor", "label": "Webservice picker de asesores"},
        {"name": "list_asesor", "label": "Webservice del listado de asesores"},
        {"name": "toggle_asesor", "label": "Webservice para cambiar estado del asesor"},
    ]
    return actions

@api_view(['POST'])
def add_asesor(request):
    """Tries to create a asesor and returns the result"""
    crud_object = Crud(AsesorSerializer, Asesor)
    return crud_object.add(request, 'add_asesor')

@api_view(['PUT'])
def replace_asesor(request, asesor_id):
    "Tries to update a asesor and returns the result"
    crud_object = Crud(AsesorSerializer, Asesor)
    return crud_object.replace(request, asesor_id, 'replace_asesor')

@api_view(['POST'])
def get_asesor(request, asesor_id):
    "Return a JSON response with asesor data for the given id"
    crud_object = Crud(AsesorSerializer, Asesor)
    return crud_object.get(request, asesor_id, 'get_asesor')

@api_view(['DELETE'])
def delete_asesor(request, asesor_id):
    """Tries to delete an asesor and returns the result."""
    crud_object = Crud(AsesorSerializer, Asesor)
    return crud_object.delete(request, asesor_id, 'delete_asesor', "Asesor elminado exitosamente")

@api_view(['POST'])
def toggle_asesor(request, asesor_id):
    """Toogles the active state for a given user"""
    crud_object = Crud(AsesorSerializer, Asesor)
    return crud_object.toggle(request, asesor_id, 'toggle_asesor', "Asesor")

@api_view(['POST'])
def picker_search_asesor(request):
    "Returns a JSON response with asesor data for a selectpicker."
    crud_object = Crud(AsesorSerializer, Asesor, data_filters.asesor_picker_filter)
    return crud_object.picker_search(request, 'picker_search_user')

@api_view(['POST'])
def list_asesor(request):
    """Returns a JSON response containing registered asesor for a datatable"""
    crud_object = Crud(AsesorSerializer, Asesor, data_filters.asesor_listing_filter)
    return crud_object.listing(request, 'list_asesor')

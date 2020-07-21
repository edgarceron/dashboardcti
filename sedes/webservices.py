"""Contains the webservices for the sedes app"""
from rest_framework.decorators import api_view
from core.crud.standard import Crud
from sedes.business_logic import data_filters
from .models import Sede
from .serializers import SedeSerializer

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_sede", "label": "Webservice crear sede"},
        {"name": "replace_sede", "label": "Webservice actualizar sede"},
        {"name": "get_sede", "label": "Webservice obtener datos sede"},
        {"name": "delete_sede", "label": "Webservice borrar sede"},
        {"name": "picker_search_sede", "label": "Webservice picker de sedes"},
        {"name": "list_sede", "label": "Webservice del listado de sedes"},
        {"name": "toggle_sede", "label": "Webservice para cambiar estado del sede"},
    ]
    return actions

@api_view(['POST'])
def add_sede(request):
    """Tries to create a sede and returns the result"""
    crud_object = Crud(SedeSerializer, Sede)
    return crud_object.add(request, 'add_sede')

@api_view(['PUT'])
def replace_sede(request, sede_id):
    "Tries to update a sede and returns the result"
    crud_object = Crud(SedeSerializer, Sede)
    return crud_object.replace(request, sede_id, 'replace_sede')

@api_view(['POST'])
def get_sede(request, sede_id):
    "Return a JSON response with sede data for the given id"
    crud_object = Crud(SedeSerializer, Sede)
    return crud_object.get(request, sede_id, 'get_sede')

@api_view(['DELETE'])
def delete_sede(request, sede_id):
    """Tries to delete an sede and returns the result."""
    crud_object = Crud(SedeSerializer, Sede)
    return crud_object.delete(request, sede_id, 'delete_sede', "Sede elminado exitosamente")

@api_view(['POST'])
def toggle_sede(request, sede_id):
    """Toogles the active state for a given user"""
    crud_object = Crud(SedeSerializer, Sede)
    return crud_object.toggle(request, sede_id, 'toggle_sede', "Sede")

@api_view(['POST'])
def picker_search_sede(request):
    "Returns a JSON response with sede data for a selectpicker."
    crud_object = Crud(SedeSerializer, Sede, data_filters.sede_picker_filter)
    return crud_object.picker_search(request, 'picker_search_user')

@api_view(['POST'])
def list_sede(request):
    """Returns a JSON response containing registered sede for a datatable"""
    crud_object = Crud(SedeSerializer, Sede, data_filters.sede_listing_filter)
    return crud_object.listing(request, 'list_sede')

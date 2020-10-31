"""Contains the webservices for the motivos app"""
from rest_framework.decorators import api_view
from core.crud.standard import Crud
from motivos.business_logic import data_filters
from .models import Motivo
from .serializers import MotivoSerializer

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_motivo", "label": "Webservice crear motivo"},
        {"name": "replace_motivo", "label": "Webservice actualizar motivo"},
        {"name": "get_motivo", "label": "Webservice obtener datos motivo"},
        {"name": "delete_motivo", "label": "Webservice borrar motivo"},
        {"name": "picker_search_motivo", "label": "Webservice picker de motivos"},
        {"name": "list_motivo", "label": "Webservice del listado de motivos"},
        {"name": "toggle_motivo", "label": "Webservice para cambiar estado del motivo"},
    ]
    return actions

@api_view(['POST'])
def add_motivo(request):
    """Tries to create a motivo and returns the result"""
    crud_object = Crud(MotivoSerializer, Motivo)
    return crud_object.add(request, 'add_motivo')

@api_view(['PUT'])
def replace_motivo(request, motivo_id):
    "Tries to update a motivo and returns the result"
    crud_object = Crud(MotivoSerializer, Motivo)
    return crud_object.replace(request, motivo_id, 'replace_motivo')

@api_view(['POST'])
def get_motivo(request, motivo_id):
    "Return a JSON response with motivo data for the given id"
    crud_object = Crud(MotivoSerializer, Motivo)
    return crud_object.get(request, motivo_id, 'get_motivo')

@api_view(['DELETE'])
def delete_motivo(request, motivo_id):
    """Tries to delete an motivo and returns the result."""
    crud_object = Crud(MotivoSerializer, Motivo)
    return crud_object.delete(request, motivo_id, 'delete_motivo', "Motivo elminado exitosamente")

@api_view(['POST'])
def toggle_motivo(request, motivo_id):
    """Toogles the active state for a given user"""
    crud_object = Crud(MotivoSerializer, Motivo)
    return crud_object.toggle(request, motivo_id, 'toggle_motivo', "Motivo")

@api_view(['POST'])
def picker_search_motivo(request):
    "Returns a JSON response with motivo data for a selectpicker."
    crud_object = Crud(MotivoSerializer, Motivo, data_filters.motivo_picker_filter)
    return crud_object.picker_search(request, 'picker_search_motivo')

@api_view(['POST'])
def list_motivo(request):
    """Returns a JSON response containing registered motivo for a datatable"""
    crud_object = Crud(MotivoSerializer, Motivo, data_filters.motivo_listing_filter)
    return crud_object.listing(request, 'list_motivo')

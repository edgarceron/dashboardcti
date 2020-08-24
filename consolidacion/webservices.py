"""Contains the webservices for the consolidacion app"""
from rest_framework.decorators import api_view
from core.crud.standard import Crud
from consolidacion.business_logic import data_filters, consolidacion_operations
from .models import Consolidacion
from .serializers import ConsolidacionSerializer, ConsolidacionListSerializer

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_consolidacion", "label": "Webservice crear consolidacion"},
        {"name": "replace_consolidacion", "label": "Webservice actualizar consolidacion"},
        {"name": "get_consolidacion", "label": "Webservice obtener datos consolidacion"},
        {"name": "delete_consolidacion", "label": "Webservice borrar consolidacion"},
        {"name": "picker_search_consolidacion", "label": "Webservice picker de consolidaciones"},
        {"name": "list_consolidacion", "label": "Webservice del listado de consolidaciones"},
        {
            "name": "toggle_consolidacion",
            "label": "Webservice para cambiar estado del consolidacion"
        },
        {
            "name": "upload_consolidacion",
            "label": "Webservice para subir consolidaciones por archivo plano"
        },
        {
            "name": "validate_cedula",
            "label": "Webservice para validar cedula antes de crear consolidación"
        },
    ]
    return actions

@api_view(['POST'])
def add_consolidacion(request):
    """Tries to create a consolidacion and returns the result"""
    if consolidacion_operations.get_user_sede(request) is None:
        return consolidacion_operations.answer_not_user_sede()
    operation = consolidacion_operations.add_sede_operation(request)
    after = consolidacion_operations.create_cf_observaciones_consolidacion
    crud_object = Crud(ConsolidacionSerializer, Consolidacion, operation, after)
    return crud_object.add(request, 'add_consolidacion')

@api_view(['PUT'])
def replace_consolidacion(request, consolidacion_id):
    "Tries to update a consolidacion and returns the result"
    operation = consolidacion_operations.add_sede_operation(request)
    crud_object = Crud(ConsolidacionSerializer, Consolidacion, operation)
    return crud_object.replace(request, consolidacion_id, 'replace_consolidacion')

@api_view(['POST'])
def get_consolidacion(request, consolidacion_id):
    "Return a JSON response with consolidacion data for the given id"
    crud_object = Crud(ConsolidacionSerializer, Consolidacion)
    return crud_object.get(request, consolidacion_id, 'get_consolidacion')

@api_view(['DELETE'])
def delete_consolidacion(request, consolidacion_id):
    """Tries to delete an consolidacion and returns the result."""
    crud_object = Crud(ConsolidacionSerializer, Consolidacion)
    return crud_object.delete(
        request, consolidacion_id,
        'delete_consolidacion', "Consolidacion elminado exitosamente"
    )

@api_view(['POST'])
def toggle_consolidacion(request, consolidacion_id):
    """Toogles the active state for a given user"""
    crud_object = Crud(ConsolidacionSerializer, Consolidacion)
    return crud_object.toggle(request, consolidacion_id, 'toggle_consolidacion', "Consolidacion")

@api_view(['POST'])
def picker_search_consolidacion(request):
    "Returns a JSON response with consolidacion data for a selectpicker."
    crud_object = Crud(
        ConsolidacionSerializer, Consolidacion,
        data_filters.consolidacion_picker_filter
    )
    return crud_object.picker_search(request, 'picker_search_user')

@api_view(['POST'])
def list_consolidacion(request):
    """Returns a JSON response containing registered consolidacion for a datatable"""
    crud_object = Crud(
        ConsolidacionListSerializer, Consolidacion,
        data_filters.consolidacion_listing_filter,
        consolidacion_operations.put_sede_motivo
    )
    return crud_object.listing(request, 'list_consolidacion')

@api_view(['POST'])
def upload_consolidacion(request):
    """Uploads a file with consolidacion data"""
    return consolidacion_operations.upload_consolidacion(request)

@api_view(['POST'])
def validate_cedula(request):
    """Validates that the given request contains a cedula for """
    return consolidacion_operations.validate_cedula(request)

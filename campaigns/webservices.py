"""Contains the webservices for the form_creator app"""
from rest_framework.decorators import api_view
from core.crud.standard import Crud
from campaigns.business_logic import data_filters, campaign_operations, manual_calls
from .models import CampaignForm, AnswersHeader, DataLlamada
from .serializers import CampaignFormSerializer, AnswersHeaderSerializer, DataLlamadaSerializar


def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_campaign", "label": "Webservice crear campaña"},
        {"name": "replace_campaign", "label": "Webservice actualizar campaña"},
        {"name": "get_campaign_manticore", "label": "Webservice obtener datos campaña"},
        {"name": "delete_campaign", "label": "Webservice borrar campaña"},
        {"name": "picker_search_campaign_manticore", "label": "Webservice picker de campañas"},
        {"name": "list_campaign", "label": "Webservice del listado de campañas"},
        {"name": "add_header", "label": "Webservice crear una cabecera de respuesta"},
        {"name": "replace_header", "label": "Webservice actualizar una cabecera de respuesta"},
        {"name": "save_answers", "label": "Webservice guardar las respuesta"},
        {"name": "add_data_llamada", "label": "Webservice para crear los datos de un usuario en llamada para encuesta"},
        {"name": "replace_data_llamada", "label": "Webservice actualizar los datos de un usuario en llamada para encuesta"},
        {"name": "fail_prepare_polls", "label": "Webservice crear nuevas llamadas a partir de las encuentas fallidas"},
    ]
    return actions

@api_view(['POST'])
def add_campaign(request):
    """Tries to create a campaign and returns the result"""
    crud_object = Crud(CampaignFormSerializer, CampaignForm)
    return crud_object.add(request, 'add_campaign')

@api_view(['PUT'])
def replace_campaign(request, campaign_id):
    "Tries to update a campaign and returns the result"
    crud_object = Crud(CampaignFormSerializer, CampaignForm)
    return crud_object.replace(request, campaign_id, 'replace_campaign')

@api_view(['POST'])
def get_campaign(request, campaign_id):
    "Return a JSON response with campaign data for the given id"
    crud_object = Crud(CampaignFormSerializer, CampaignForm)
    return crud_object.get(request, campaign_id, 'get_campaign_manticore')

@api_view(['DELETE'])
def delete_campaign(request, campaign_id):
    """Tries to delete an campaign and returns the result."""
    crud_object = Crud(CampaignFormSerializer, CampaignForm)
    return crud_object.delete(request, campaign_id, 'delete_campaign', "Campaña elminada exitosamente")

@api_view(['POST'])
def toggle_campaign(request, campaign_id):
    """Toogles the active state for a given user"""
    crud_object = Crud(CampaignFormSerializer, CampaignForm)
    return crud_object.toggle(request, campaign_id, 'toggle_campaign', "Campaña")

@api_view(['POST'])
def picker_search_campaign(request):
    "Returns a JSON response with campaign data for a selectpicker."
    crud_object = Crud(CampaignFormSerializer, CampaignForm, data_filters.campaign_picker_filter)
    return crud_object.picker_search(request, 'picker_search_campaign_manticore')

@api_view(['POST'])
def list_campaign(request):
    """Returns a JSON response containing registered campaign for a datatable"""
    crud_object = Crud(CampaignFormSerializer, CampaignForm, data_filters.campaign_listing_filter)
    return crud_object.listing(request, 'list_campaign')

@api_view(['POST'])
def upload_calls_campaign(request):
    """Uploads the calls for the campaign"""
    return campaign_operations.upload_calls_campaign(request)

@api_view(['POST'])
def add_header(request):
    """Tries to create a header and returns the result"""
    crud_object = Crud(AnswersHeaderSerializer, AnswersHeader)
    return crud_object.add(request, 'add_header')

@api_view(['POST'])
def replace_header(request, header_id):
    """Tries to update a header and returns the result"""
    crud_object = Crud(AnswersHeaderSerializer, AnswersHeader)
    return crud_object.replace(request, header_id, 'replace_header')

@api_view(['POST'])
def save_answers(request, header_id):
    """Tries to update a header and returns the result"""
    return campaign_operations.save_answers(request, header_id)


@api_view(['POST'])
def add_data_llamada(request):
    """Tries to create a header and returns the result"""
    operation = manual_calls.create_call
    crud_object = Crud(DataLlamadaSerializar, DataLlamada, operation)
    return crud_object.add(request, 'add_data_llamada')

@api_view(['POST'])
def replace_data_llamada(request, data_llamada_id):
    """Tries to update a header and returns the result"""
    crud_object = Crud(DataLlamadaSerializar, DataLlamada)
    return crud_object.replace(request, data_llamada_id, 'replace_data_llamada')

@api_view(['POST'])
def data_chart(request):
    """Returns the data to create charts for every questions"""
    return campaign_operations.data_chart(request)

@api_view(['POST'])
def fail_prepare_polls(request):
    """Create new Header for failed AnswerHeaders in a given date range"""
    return campaign_operations.fail_prepare_polls(request)

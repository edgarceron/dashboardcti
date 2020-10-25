"""Contains the webservices for the form_creator app"""
from rest_framework.decorators import api_view
from core.crud.standard import Crud
from campaigns.business_logic import data_filters, campaign_operations
from .models import CampaignForm
from .serializers import CampaignFormSerializer


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
    return crud_object.get(request, campaign_id, 'get_campaign')

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
    return crud_object.picker_search(request, 'picker_search_campaign')

@api_view(['POST'])
def list_campaign(request):
    """Returns a JSON response containing registered campaign for a datatable"""
    crud_object = Crud(CampaignFormSerializer, CampaignForm, data_filters.campaign_listing_filter)
    return crud_object.listing(request, 'list_campaign')

@api_view(['POST'])
def upload_calls_campaign(request):
    """Uploads the calls for the campaign"""
    return campaign_operations.upload_calls_campaign(request)
    
"Contains the views for the form_creator app."
import os
from django.shortcuts import render, redirect, HttpResponse
from users.permission_validation import PermissionValidation
from campaigns.business_logic import show_results, fail_management
from .models import CampaignForm


def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "form_campaign", "label": "Pagina del formulario de camapaña"},
        {"name": "listing_campaign", "label": "Pagina del listado de campañas"},
        {"name": "upload_data_campaign", "label": "Pagina para subir datos a la camapaña"},
        {"name": "download_poll_answers", "label": "Descargar datos de campaña"},
        {"name": "download_fails_polls", "label": "Descargar datos de encuestas fallidas"},
        {"name": "data_campaign", "label": "Pagina ver datos de la campaña"},
    ]
    return actions

def form_campaign(request, campaign_id=0):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_campaign')
    if validation['status']:
        if campaign_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'campaigns/form.html',
            {
                'id':campaign_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def listing_campaign(request):
    "Returns the rendered template for campaign listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_campaign')
    if validation['status']:
        return render(
            request,
            'campaigns/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def upload_data_campaign(request, campaign_id):
    """Shows the rendered template for campaign data upload"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('upload_data_campaign')
    if validation['status']:
        campaign = CampaignForm.objects.get(id=campaign_id)
        return render(
            request,
            'campaigns/upload_data.html',
            {
                'id':campaign_id,
                'campaign_name':campaign.name,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def download_poll_answers(request, campaign_id, start_date, end_date):
    """Creates a csv file which contains the campaign answers and returns a file response with
    the file"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('download_poll_answers')
    if validation['status']:
        collected_data = show_results.collect_data(campaign_id, start_date, end_date)
        file_path = show_results.data_to_csv(collected_data)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        return render(request, 'maingui/http_error.html', None, status=404)
    return permission_obj.error_response_view(validation, request)

def download_fails_polls(request, campaign, start_date, end_date):
    """Creates a csv file which contains the failed consolidations"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('download_fails_polls')
    if validation['status']:
        collected_data = fail_management.check_fails(campaign, start_date, end_date)
        file_path = show_results.data_to_csv(collected_data)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        return render(request, 'maingui/http_error.html', None, status=404)
    return permission_obj.error_response_view(validation, request)

def data_campaign(request, campaign_id):
    """Shows the view for campaign data"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('data_campaign')
    if validation['status']:
        campaign = CampaignForm.objects.get(id=campaign_id)
        return render(
            request,
            'campaigns/data_campaign.html',
            {
                'id':campaign_id,
                'campaign_name':campaign.name,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

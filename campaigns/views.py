"Contains the views for the form_creator app."
from django.shortcuts import render, redirect
from users.permission_validation import PermissionValidation
from .models import CampaignForm

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "form_campaign", "label": "Pagina del formulario de camapaña"},
        {"name": "listing_campaign", "label": "Pagina del listado de campañas"},
        {"name": "upload_data_campaign", "label": "Pagina para subir datos a la camapaña"},
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

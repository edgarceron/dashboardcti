"Contains the views for the form_creator app."
from django.shortcuts import render, redirect
from users.permission_validation import PermissionValidation

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "campaign_form", "label": "Pagina del formulario de camapaña"},
        {"name": "listing_campaign", "label": "Pagina del listado de campañas"}
    ]
    return actions

def campaign_form(request, campaign_id=0):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('campaign_campaign')
    if validation['status']:
        if campaign_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'forms/form.html',
            {
                'id':campaign_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)

def listing_campaign(request):
    "Returns the rendered template for campaign listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_campaign')
    if validation['status']:
        return render(
            request,
            'forms/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)

"""Manages the views for motivos module"""
from django.shortcuts import render
from users.permission_validation import PermissionValidation

# Create your views here.
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {
            "name": "listing_motivo",
            "label": "Pagina de listado del modulo de motivos de entrada a taller"
        },
        {
            "name": "form_motivo",
            "label": "Pagina de formulario del modulo de motivos de entrada a taller"
        }
    ]
    return actions

def form_motivo(request, motivo_id=0):
    "Returns the rendered template for the given motivo."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_motivo')
    if validation['status']:
        if motivo_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'motivos/form.html',
            {
                'id':motivo_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def listing_motivo(request):
    "Returns the rendered template for motivo listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_motivo')
    if validation['status']:
        return render(
            request,
            'motivos/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

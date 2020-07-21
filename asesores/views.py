"""Manages the views for asesores app"""
from django.shortcuts import render
from users.permission_validation import PermissionValidation

# Create your views here.
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {
            "name": "listing_asesor",
            "label": "Pagina de listado del modulo de asesores de taller"
        },
        {
            "name": "form_asesor",
            "label": "Pagina de formulario del modulo de asesores de taller"
        }
    ]
    return actions

def form_asesor(request, asesor_id=0):
    "Returns the rendered template for the given asesor."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_asesor')
    if validation['status']:
        if asesor_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'asesores/form.html',
            {
                'id':asesor_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def listing_asesor(request):
    "Returns the rendered template for asesor listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_asesor')
    if validation['status']:
        return render(
            request,
            'asesores/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

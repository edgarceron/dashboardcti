"""Manages the views for sedes module"""
from django.shortcuts import render
from users.permission_validation import PermissionValidation

# Create your views here.
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {
            "name": "listing_sede",
            "label": "Pagina de listado del modulo de sedes de entrada a taller"
        },
        {
            "name": "form_sede",
            "label": "Pagina de formulario del modulo de sedes de entrada a taller"
        }
    ]
    return actions

def form_sede(request, sede_id=0):
    "Returns the rendered template for the given sede."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_sede')
    if validation['status']:
        if sede_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'sedes/form.html',
            {
                'id':sede_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def listing_sede(request):
    "Returns the rendered template for sede listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_sede')
    if validation['status']:
        return render(
            request,
            'sedes/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

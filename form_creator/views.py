"Contains the views for the form_creator app."
from django.shortcuts import render, redirect
from users.permission_validation import PermissionValidation

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "form_form", "label": "Pagina del formulario de formulario"},
        {"name": "listing_form", "label": "Pagina del listado de formullarios"}
    ]
    return actions

def form_form(request, form_id=0):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_form')
    if validation['status']:
        if form_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'form_creator/form.html',
            {
                'id':form_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def listing_form(request):
    "Returns the rendered template for form listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_form')
    if validation['status']:
        return render(
            request,
            'form_creator/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def draw(request):
    "Returns the rendered template for form listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_form')
    if validation['status']:
        return render(
            request,
            'form_creator/draw.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)
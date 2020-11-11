"""Manages the views for consolidacion module"""
import os
from django.shortcuts import render, HttpResponse
from consolidacion.business_logic import show_results
from users.permission_validation import PermissionValidation

# Create your views here.
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {
            "name": "listing_consolidacion",
            "label": "Pagina de listado del modulo de consolidaciones de entrada a taller"
        },
        {
            "name": "form_consolidacion",
            "label": "Pagina de formulario del modulo de consolidaciones de entrada a taller"
        },
        {
            "name": "upload_consolidacion_form",
            "label": "Pagina de formulario para subir consolidaciones por archivo plano"
        },
        {
            "name": "turnero",
            "label": "Pagina para mostrar los turnos de una sede"
        },
        {
            "name": "download_consolidaciones",
            "label": "Descargar csv de consolidaciones"
        },
        {
            "name": "datos_consolidacion",
            "label": "Pagina resultados de consolidación"
        },
    ]
    return actions

def form_consolidacion(request, consolidacion_id=0):
    "Returns the rendered template for the given consolidacion."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_consolidacion')
    if validation['status']:
        if consolidacion_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'consolidacion/form.html',
            {
                'id':consolidacion_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def upload_consolidacion_form(request):
    "Returns the rendered template for the consolidacion upload form."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('upload_consolidacion_form')
    if validation['status']:

        return render(
            request,
            'consolidacion/upload_form.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def listing_consolidacion(request):
    "Returns the rendered template for consolidacion listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_consolidacion')
    if validation['status']:
        return render(
            request,
            'consolidacion/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def turnero(request):
    """Return the template for the turnero"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('turnero')
    if validation['status']:
        return render(
            request,
            'consolidacion/turnero.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def download_consolidaciones(request, agent, start_date, end_date):
    """Creates a csv file which contains the campaign answers and returns a file response with
    the file"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('download_consolidaciones')
    if validation['status']:
        collected_data = show_results.collect_data(agent, start_date, end_date)
        file_path = show_results.data_to_csv(collected_data)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        return render(request, 'maingui/http_error.html', None, status=404)
    return permission_obj.error_response_view(validation, request)

def datos_consolidacion(request):
    """Shows the view for campaign data"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('datos_consolidacion')
    if validation['status']:
        return render(
            request,
            'campaigns/datos_consolidacion.html',
            {
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

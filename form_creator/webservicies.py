"""Contains the webservices for the form_creator app"""
import datetime
import pytz
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.permission_validation import PermissionValidation
from .models import Form
from .webservicies import FormSerializer

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_form", "label": "Webservice crear formulario"},
        {"name": "replace_form", "label": "Webservice actualizar formulario"},
        {"name": "get_form", "label": "Webservice obtener datos formulario"},
        {"name": "delete_form", "label": "Webservice borrar formulario"},
        {"name": "picker_search_form", "label": "Webservice picker de formularios"},
        {"name": "list_form", "label": "Webservice del listado de formularios"},
        {"name": "toggle_form", "label": "Webservice para cambiar estado del formulario"},
        {"name": "create_question", "label": "Webservice crear pregunta"},
        {"name": "replace_question", "label": "Webservice actualizar pregunta"},
        {"name": "delete_question", "label": "Webservice borrar pregunta"},
        {"name": "change_question_position", "label": "Webservice cambiar posición de la pregunta"},
        {"name": "create_answer", "label": "Webservice crear respuesta"},
        {"name": "replace_answer", "label": "Webservice actualizar respuesta"},
        {"name": "delete_answer", "label": "Webservice borrar respuesta"}
    ]
    return actions

@api_view(['POST'])
def add_form(request):
    """Tries to create an profile and returns the result"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('add_profile')
    if validation['status']:
        data = request.data.copy()
        form_serializer = FormSerializer(data=data)
        if form_serializer.is_valid():
            form_serializer.save()
            return Response(
                {"success":True, "user_id":form_serializer.data['id']},
                status=status.HTTP_201_CREATED,
                content_type='application/json')

        data = error_data(form_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['PUT'])
def replace_form(request, form_id):
    "Tries to update a form and returns the result"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('replace_user')
    if validation['status']:
        form_obj = Form.objects.get(id=form_id)
        data = request.data.copy()
        form_serializer = FormSerializer(form_obj, data=data)

        if form_serializer.is_valid():
            form_serializer.save()
            return Response(
                {"success":True, "form_id":form_id},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )

        data = error_data(form_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def get_form(request, form_id):
    "Return a JSON response with form data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_user')
    if validation['status']:
        form_obj = Form.objects.get(id=form_id)
        form_serializer = FormSerializer(form_obj)
        form_data = form_serializer.data.copy()

        data = {
            "success":True,
            "data":form_data
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['DELETE'])
def delete_form(request, form_id):
    """Tries to delete an user and returns the result."""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_user')
    if validation['status']:
        form_obj = Form.objects.get(id=form_id)
        form_obj.delete()
        data = {
            "success": True,
            "message": "Usuario elminado exitosamente"
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def toggle_form(request, form_id):
    """Toogles the active state for a given user"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('toggle_user')

    if validation['status']:
        form_obj = Form.objects.get(id=form_id)
        previous = form_obj.active

        if previous:
            message = "Formulario desactivado con exito"
        else:
            message = "Formulario activado con exito"

        form_obj.active = not form_obj.active
        form_obj.save()
        data = {
            "success": True,
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def picker_search_form(request):
    "Returns a JSON response with form data for a selectpicker."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('picker_search_profile')
    if validation['status']:
        value = request.data['value']
        queryset = Form.form_picker_filter(value)
        serializer = FormSerializer(queryset, many=True)
        result = serializer.data

        data = {
            "success": True,
            "result": result
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def list_form(request):
    """ Returns a JSON response containing registered users"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('list_profile')
    if validation['status']:
        sent_data = request.data
        draw = int(sent_data['draw'])
        start = int(sent_data['start'])
        length = int(sent_data['length'])
        search = sent_data['search[value]']

        records_total = Form.objects.count()

        if search != '':
            queryset = Form.form_listing_filter(search, start, length)
            records_filtered = Form.form_listing_filter(search, start, length, True)
        else:
            queryset = Form.objects.all()[start:start + length]
            records_filtered = records_total


        result = FormSerializer(queryset, many=True)
        data = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': result.data
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def create_question(request):
    pass 

@api_view(['PUT'])
def replace_question(request, question_id):
    pass

@api_view(['POST'])
def delete_question(request):
    pass 

@api_view(['POST'])
def change_question_position(request):
    pass 

@api_view(['POST'])
def create_asnwer(request):
    pass 

@api_view(['PUT'])
def replace_asnwer(request, asnwer_id):
    pass

@api_view(['POST'])
def delete_asnwer(request):
    pass

def error_data(serializer):
    """Return a common JSON error result"""
    error_details = []
    for key in serializer.errors.keys():
        error_details.append({"field": key, "message": serializer.errors[key][0]})

    data = {
        "Error": {
            "success": False,
            "status": 400,
            "message": "Los datos enviados no son validos",
            "details": error_details
        }
    }
    return data

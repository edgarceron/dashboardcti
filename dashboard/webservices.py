"""Contains the webservices for the maingui app"""
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.permission_validation import PermissionValidation
from agent_console.models import AgentConsoleOptions
from dashboard.business_logic import data_process

# Create your views here.
def get_actions():
    actions = [
        {
            "name": "replace_options_dashboard",
            "label": "Webservice para actualizar opciones dashboard"
        },
        {
            "name": "get_options_dashboard",
            "label": "Webservice para obtener valores de las opciones del dashboard"
        },
        {
            "name": "get_data_dashboard",
            "label": "Webservice para obtener valores del dashboard"
        },
    ]
    return actions

@api_view(['PUT'])
def replace_options_dashboard(request):
    "Tries to update the agent console options"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('replace_options_dashboard')
    if validation['status']:
        data = request.data.copy()
        print(data)
        redirection_time = data['TMOTIME']

        try:
            option_tmotime = AgentConsoleOptions.objects.get(option='TMOTIME')
        except AgentConsoleOptions.DoesNotExist:
            option_tmotime = AgentConsoleOptions()
            option_tmotime.option = 'TMOTIME'

        option_tmotime.value = redirection_time

        option_tmotime.save()

        return Response(
            {"success":True},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def get_options_dashboard(request):
    "Return a JSON response with user data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_options_dashboard')
    if validation['status']:
        try:
            option_tmotime = AgentConsoleOptions.objects.get(option='TMOTIME')
        except AgentConsoleOptions.DoesNotExist:
            option_tmotime = AgentConsoleOptions()
            option_tmotime.option = 'TMOTIME'

        options = {
            option_tmotime.option: option_tmotime.value
        }

        data = {
            "success":True,
            "data":options
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def get_data_dashboard(request):
    "Return a JSON response with user data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_data_dashboard')
    if validation['status']:
        data = data_process.data_process(request)

        return Response(
            data,
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

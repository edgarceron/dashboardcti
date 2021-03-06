""" Webservices for the agent_console app """
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.crud.standard import Crud
from users.permission_validation import PermissionValidation
from agent_console.business_logic import data_filters
from consolidacion.business_logic import citas
from .console_functions.agent_state import AgentState
from .console_functions.generate_users import GenerateUsers
from .console_functions import create_calls_consolidacion
from .serializers import AgentSerializer, CampaignSerializer, CampaignEntrySerializer, BreakTimesSerializer
from .models import Agent, AgentConsoleOptions, Campaign, CampaignEntry, BreakTimes
from .business_logic import user_extra_fields

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "set_user_agent", "label": "Webservice enlazar usuario con agente de call center"},
        {"name": "picker_search_agent", "label": "Webservice para actualizar el picker de agentes"},
        {"name": "get_agent", "label": "Webservice para obteber los datos del agente"},
        {"name": "get_user_sede", "label": "Webservice para obteber los datos de la sede del usuario"},
        {"name": "agent_state", "label": "Webservice para obteber el estado del agente"},
        {"name": "get_crm_url", "label": "Webservice para obteber la url de redirección al CRM"},
        {
            "name": "replace_options_agent_console",
            "label": "Webservice para guardar las opciones de la consola de agente"},
        {
            "name": "get_options_agent_console",
            "label": "Webservice para obtener las opciones de la consola de agente"},
        {
            "name": "auto_generate_users",
            "label": "Webservice para generar los usuario automaticamente"
        },
        {
            "name": "set_user_sede",
            "label": "Webservice para enlazar un usuario con una sede"
        },
        {
            "name": "picker_search_campaign",
            "label": "Webservice para actualizar el picker de campañas salientes"
        },
        {
            "name": "picker_search_campaign_entry",
            "label": "Webservice para actualizar el picker de campañas entrantes"
        },
        {
            "name": "get_campaign",
            "label": "Webservice para obteber los datos de una campaña saliente"
        },
        {
            "name": "get_campaign_entry",
            "label": "Webservice para obteber los datos de una campaña entrante"
        },
        {
            "name": "create_cita",
            "label": "Webservice para crear cita en dms"
        },
        {
            "name": "check_horarios",
            "label": "Webservice para verificar horarios disponibles"
        },
        {
            "name": "send_confirmation_mail",
            "label": "Webservice para enviar correo de confirmación"
        },
        {
            "name": "create_calls_asterisk",
            "label": "Webservice para generar llamadas de consolidación en el asterisk"
        },
        {
            "name": "add_break2",
            "label": "Webservice para guardar breaks"
        },
        {
            "name": "check_citas_horario",
            "label": "Webservice para mostrar las citas agendadas para una sede en el horario dado"
        },
    ]
    return actions

@api_view(['PUT'])
def add_break2(request):
    """Breaks."""
    return Response({"message": "Got some data!", "data": request.data})    

@api_view(['POST'])
def set_user_agent(request):
    """Tries to associate an user with an agent and returns the result"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('set_user_agent')
    if validation['status']:
        return user_extra_fields.set_unset_user_agent(request)
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def picker_search_agent(request):
    "Returns a JSON response with user data for a selectpicker."
    crud_object = Crud(AgentSerializer, Agent, data_filters.agent_picker_filter)
    return crud_object.picker_search(request, 'picker_search_agent')

@api_view(['POST'])
def get_agent(request, user_id):
    "Return a JSON response with agent data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_agent')
    if validation['status']:
        return user_extra_fields.get_agent(request, user_id)
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def get_user_sede(request, user_id):
    "Return a JSON response with user_sede data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_user_sede')
    if validation['status']:
        return user_extra_fields.get_user_sede(request, user_id)
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def agent_state(request):
    """Gets the agent state"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('agent_state')
    if validation['status']:
        agent_state_obj = AgentState(False)
        data = request.data
        previous_state = data['previous_state']
        id_agent = data['id_agent']
        previous_call = data['previous_call']
        previous_break = data['previous_break']

        state, current_call_entry, current_call, active_break = agent_state_obj.check_state(id_agent)
        if (
                state != previous_state
                or previous_break != active_break
                or (state == 4 and current_call_entry.uniqueid != previous_call)
                or (state == 5 and current_call.uniqueid != previous_call)
        ):
            answer = agent_state_obj.get_answer(state, id_agent, current_call_entry, current_call)
        else:
            answer = {'update': False}

        return Response(answer, status=status.HTTP_200_OK, content_type='application/json')

    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def get_crm_url(request):
    """Gets the agent state"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_crm_url')
    if validation['status']:
        try:
            option = AgentConsoleOptions.objects.get(option='CRM_URL')
            data = {
                'success': True,
                'url': option.value
            }
        except AgentConsoleOptions.DoesNotExist:
            data = {
                'success': False,
                'url': "No se ha especificado un valor para la url de redirección"
            }

        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    return permission_obj.error_response_webservice(validation, request)

@api_view(['PUT'])
def replace_options_agent_console(request):
    "Tries to update the agent console options"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('replace_options_agent_console')
    if validation['status']:
        data = request.data.copy()
        print(data)
        redirection_time = data['CAMPAIGN_CONSOLIDACION']

        try:
            option_campaign = AgentConsoleOptions.objects.get(option='CAMPAIGN_CONSOLIDACION')
        except AgentConsoleOptions.DoesNotExist:
            option_campaign = AgentConsoleOptions()
            option_campaign.option = 'CAMPAIGN_CONSOLIDACION'


        option_campaign.value = redirection_time

        option_campaign.save()

        return Response(
            {"success":True},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def get_options_agent_console(request):
    "Return a JSON response with user data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_options_agent_console')
    if validation['status']:
        try:
            option_campaign = AgentConsoleOptions.objects.get(option='CAMPAIGN_CONSOLIDACION')
        except AgentConsoleOptions.DoesNotExist:
            option_campaign = AgentConsoleOptions()
            option_campaign.option = 'CAMPAIGN_CONSOLIDACION'

        options = {
            option_campaign.option: option_campaign.value
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
def auto_generate_users(request):
    "Return a JSON response with user data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('auto_generate_users')
    if validation['status']:
        try:
            GenerateUsers.bulk_create_users()
            return Response(
                {'success':True, 'message':'Usuarios Generados con exito'},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )
        except:
            return Response(
                {'success':False, 'message':'Ocurrio un error al intentar generar los usuarios'},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )

    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def set_user_sede(request):
    """Tries to associate an user with a sede and returns the result"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('set_user_agent')
    if validation['status']:
        return user_extra_fields.set_unset_user_sede(request)
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def get_campaign(request, campaign_id):
    "Return a JSON response with campaign data for the given id"
    crud_object = Crud(CampaignSerializer, Campaign)
    return crud_object.get(request, campaign_id, 'get_campaign')

@api_view(['POST'])
def get_campaign_entry(request, campaign_id):
    "Return a JSON response with campaign data for the given id"
    crud_object = Crud(CampaignEntrySerializer, CampaignEntry)
    return crud_object.get(request, campaign_id, 'get_campaign_entry')

@api_view(['POST'])
def picker_search_campaign(request):
    "Returns a JSON response with campaign data for a selectpicker."
    crud_object = Crud(CampaignSerializer, Campaign, data_filters.campaign_picker_filter)
    return crud_object.picker_search(request, 'picker_search_campaign')

@api_view(['POST'])
def picker_search_campaign_entry(request):
    "Returns a JSON response with campaign data for a selectpicker."
    crud_object = Crud(
        CampaignEntrySerializer, CampaignEntry, data_filters.campaign_entry_picker_filter)
    return crud_object.picker_search(request, 'picker_search_campaign_entry')

@api_view(['POST'])
def create_cita(request):
    "Tries to create a cita a return the result."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('create_cita')
    if validation['status']:
        return citas.create_cita(request)
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def check_horarios(request):
    """Validates that the given request contains a cedula for """
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('check_horarios')
    if validation['status']:
        data = request.data
        sede = data['sede']
        fecha = data['fecha']
        return citas.verificar_horarios(sede, fecha)
    return permission_obj.error_response_webservice(validation, request)


@api_view(['POST'])
def check_horarios(request):
    """Validates that the given request contains a cedula for """
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('check_horarios')
    if validation['status']:
        data = request.data
        sede = data['sede']
        fecha = data['fecha']
        return citas.verificar_horarios(sede, fecha)
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def check_citas_horario(request):
    """Validates that the given request contains a cedula for """
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('check_citas_horario')
    if validation['status']:
        data = request.data
        sede = data['sede']
        fecha = data['fecha']
        hora = data['hora']
        return citas.citas_en_horario(sede, fecha, hora)
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def send_confirmation_mail(request):
    """Validates that the given request contains a cedula for """
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('send_confirmation_mail')
    if validation['status']:
        send = citas.create_mail_and_send(request.data)
        if send['status']:
            success = True
        else:
            success = False
        return Response(
            {'success':success, 'mail': send['mail']},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

@api_view(['POST'])
def create_calls_asterisk(request):
    """Validates that the given request contains a cedula for """
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('create_calls_asterisk')
    if validation['status']:
        create_calls_consolidacion.create_calls_consolidacion()
        return Response(
            {'success':True, 'message':'Llamadas generadas con exito'},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)


@api_view(['POST'])
def save_break_times(request):
    """Saves break times"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('create_calls_asterisk')
    if validation['status']:
        data_json = request.data['breaks']
        data = json.loads(data_json)
        error_data = []
        for break_time_data in data:
            try:
                break_time = BreakTimes.objects.get(id_break=break_time_data['id_break'])
                serializer = BreakTimesSerializer(break_time, data=break_time_data)
            except BreakTimes.DoesNotExist:
                serializer = BreakTimesSerializer(data=break_time_data)
            
            if serializer.is_valid():
                serializer.save()
            else:
                error_data.append(Crud.error_data(serializer)['Error']['details'])
            
        data = {
            "success": True,
            "message": "Tiempos guardados",
            "Error": {
                "details": error_data
            }
        }
        
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)

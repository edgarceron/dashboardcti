"""Manages the extra info for a user"""
from rest_framework.response import Response
from rest_framework import status
from sedes.models import Sede
from sedes.serializers import SedeSerializer
from agent_console.models import UserAgent, Agent, UserSede
from users.models import User
from agent_console.serializers import UserAgentSerializer, UserSedeSerializer
from core.crud.standard import Crud

def set_unset_user_agent(request):
    """Sets or unsent the agent id for an agent"""
    data = request.data
    user_id = data['user']
    agent_id = data['agent']
    if agent_id == "":
        return Response(
            {"success":True},
            status=status.HTTP_200_OK,
            content_type='application/json')
    else:
        try:
            query = UserAgent.objects.filter(user=user_id)
            if len(query) > 0:
                for obj in query:
                    model = obj
                    if agent_id == "":
                        model.delete()
                        return Response(
                            {"success":True, "message":"UserAgent deleted"},
                            status=status.HTTP_200_OK,
                            content_type='application/json')

                    serializer = UserAgentSerializer(instance=model, data=data)

            else:
                serializer = UserAgentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success":True},
                    status=status.HTTP_201_CREATED,
                    content_type='application/json')
            data = Crud.error_data(serializer)
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json')
        except Agent.DoesNotExist:
            data = {
                'success': False,
                'message': 'El agente se borro del servidor de telefonía, intente con otro agente'
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')

def set_unset_user_sede(request):
    data = request.data.copy()
    try:
        user_id = data['user']
        user_sede_obj = UserSede.objects.get(user=user_id)
        user_sede_serializer = UserSedeSerializer(user_sede_obj, data=data)
    except UserSede.DoesNotExist:
        user_sede_serializer = UserSedeSerializer(data=data)

    if user_sede_serializer.is_valid():
        user_sede_serializer.save()
        return Response(
            {"success":True, "id":user_sede_serializer.data['id']},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    elif data['sede'] == None:
        user_sede_obj.delete()
        return Response(
            {"success": True, "message":"Usuario se guarda sin sede"},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    else:
        return Response(
            {
                "success": False, 
                "message":"Ocurrio un error al intentar guardar la sede del usuario"
            },
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

def get_agent(request, user_id):
    "Return a JSON response with agent data for the given id"
    try:
        user_agent_obj = UserAgent.objects.get(user=user_id)
        agent_id = user_agent_obj.agent
        agent_obj = Agent.objects.get(id=agent_id)
        agent_serializer = AgentSerializer(agent_obj)
        agent_data = agent_serializer.data.copy()

        data = {
            "success":True,
            "data":agent_data
        }
    except:
        data = {
            "success":False
        }

    return Response(
        data,
        status=status.HTTP_200_OK,
        content_type='application/json'
    )

def get_user_sede(request, user_id):
    "Return a JSON response with sede data for the given id"
    try:
        user_sede_obj = UserSede.objects.get(user=user_id)
        sede_obj = user_sede_obj.sede
        sede_serializer = SedeSerializer(sede_obj)
        sede_data = sede_serializer.data.copy()

        data = {
            "success":True,
            "data":sede_data
        }
    except UserSede.DoesNotExist:
        data = {
            "success":False
        }

    return Response(
        data,
        status=status.HTTP_200_OK,
        content_type='application/json'
    )

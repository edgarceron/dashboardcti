"""Contains the webservices for the users app"""
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSerializer, BasicUserSerializer
from .models import User


def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_user", "label": "Webservice crear usuario"},
        {"name": "replace_user", "label": "Webservice actualizar usuario"},
        {"name": "get_user", "label": "Webservice obtener datos usuario"},
        {"name": "delete_user", "label": "Webservice borrar usuario"},
        {"name": "picker_search_user", "label": "Webservice picker de usuarios"},
        {"name": "list_user", "label": "Webservice del listado de usuarios"},
        {"name": "toggle_user", "label": "Webservice para cambiar estado del usuario"},
    ]
    return actions

@api_view(['POST'])
def add_user(request):
    """Tries to create an user and returns the result"""
    #TODO verificar usuario y permisos
    user_serializer = UserSerializer(data = request.data)
    if user_serializer.is_valid():
        user_serializer.save()
        return Response(
            {"success":True}, 
            status=status.HTTP_201_CREATED, content_type='application/json')

    data = error_data(user_serializer)
    return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(['PUT'])
def replace_user(request, user_id):
    "Tries to update an user and returns the result"
    #TODO verificar usuario y permisos
    user_obj = User.objects.get(id=user_id)
    user_serializer = UserSerializer(user_obj, data=request.data)

    if user_serializer.is_valid():
        user_serializer.save()
        return Response(
            {"success":True},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    data = error_data(user_serializer)
    return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(['POST'])
def get_user(request, user_id):
    "Return a JSON response with user data for the given id"
    #TODO verificar usuario y permisos
    user_obj = User.objects.get(id=user_id)
    user_serializer = UserSerializer(user_obj)

    data = {
        "success":True,
        "data": user_serializer.data
    }
 

    return Response(
        data,
        status=status.HTTP_200_OK,
        content_type='application/json'
    )

@api_view(['DELETE'])
def delete_user(request, user_id):
    """Tries to delete an user and returns the result."""
    #TODO verificar usuario y permisos
    user_obj = User.objects.get(id=user_id)
    user_obj.delete()
    data = {
        "success": True,
        "message": "Usuario elminado exitosamente"
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

@api_view(['POST'])
def toggle_user(request, user_id):
    """Toogles the active state for a given user"""
    #TODO verificar usuario y permisos
    user_obj = User.objects.get(id=user_id)
    previous = user_obj.active

    if previous:
        message = "Usuario desactivado con exito"
    else:
        message = "Usuario activado con exito"

    user_obj.active = not user_obj.active
    user_obj.save()
    data = {
        "success": True,
        "message": message
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

@api_view(['POST'])
def picker_search_user(request):
    "Returns a JSON response with user data for a selectpicker."
    #TODO verificar usuario y permisos
    value = request.data['value']
    #result     = User.usersPickerFilter(value)
    queryset = User.usersPickerFilter(value)
    serializer = BasicUserSerializer(queryset, many=True)
    result = serializer.data

    data = {
        "success": True,
        "result": result
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
def list_user(request):
    """ Returns a JSON response containing registered users"""
    sent_data = request.data
    draw = int(sent_data['draw'])
    start = int(sent_data['start'])
    length = int(sent_data['length'])
    search = sent_data['search[value]']

    records_total = User.objects.count()

    print(start)
    print(length)

    if search != '':
        queryset = User.users_listing_filter(search, start, length)
        records_filtered = User.users_listing_filter(search, start, length, True)
    else:
        queryset = User.objects.all()[start:start + length]
        records_filtered = records_total


    result = BasicUserSerializer(queryset, many=True)
    data = {
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'data': result.data
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')


def error_data(user_serializer):
    """Return a common JSON error result"""
    error_details = []
    for key in user_serializer.errors.keys():
        error_details.append({"field": key, "message": user_serializer.errors[key][0]})

    data = {
        "Error": {
            "success": False,
            "status": 400,
            "message": "Los datos enviados no son validos",
            "details": error_details
        }
    }
    return data
    
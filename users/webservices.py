from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, BasicUserSerializer
from .models import User
from rest_framework import status

def get_actions():
    actions = [
       {"name": "add_user", "label": "Webservice crear usuario"},
       {"name": "replace_user", "label": "Webservice actualizar usuario"},
       {"name": "delete_user", "label": "Webservice borrar usuario"},
       {"name": "picker_search_user", "label": "Webservice picker de usuarios"},
    ]
    return actions

@api_view(['POST'])
def add_user(request):
    #TODO verificar usuario y permisos
    user_serializer = UserSerializer(data = request.data)
    if(user_serializer.is_valid()):
        user_serializer.create()
        return Response({"success":True}, status=status.HTTP_201_CREATED, content_type='application/json')
    else:
        data = error_data(user_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(['POST'])
def replace_user(request, id):
    #TODO verificar usuario y permisos
    user_obj = User.objects.get(id = id)
    user_serializer = UserSerializer(user_obj, data=request.data)

    if(user_serializer.is_valid()):
        user_serializer.save()
        return Response({"success":True}, status=status.HTTP_200_OK, content_type='application/json')

    else:
        data = error_data(user_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(['DELETE'])
def delete_user(request, id):
    #TODO verificar usuario y permisos
    user_obj = User.objects.get(id = id)
    user_obj.delete()
    data = {
        "success": True,
        "message": "Usuario elminado exitosamente"
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

@api_view(['POST'])
def picker_search_user(request):
    #TODO verificar usuario y permisos
    value      = request.data['value']
    #result     = User.usersPickerFilter(value)
    queryset   = User.usersPickerFilter(value)
    serializer = BasicUserSerializer(queryset, many=True)
    result     = serializer.data

    data   = {
        "success": True,
        "result": result
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

def error_data(user_serializer):
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
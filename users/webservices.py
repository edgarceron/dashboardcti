"""Contains the webservices for the users app"""

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from core.crud.standard import Crud
from users.business_logic import login_management
from users.business_logic import data_filters
from users.business_logic import user_management
from .serializers import UserSerializer, BasicUserSerializer
from .models import User
from .permission_validation import PermissionValidation


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
        {"name": "get_own", "label": "Webservice obtener datos del usuario logeado actualemente"},
        {"name": "replace_own", "label": "Webservice actualizar usuario logeado actualemente"},
    ]
    return actions

@api_view(['POST'])
def add_user(request):
    """Tries to create an user and returns the result"""
    crud_object = Crud(UserSerializer, User, login_management.password_encode)
    return crud_object.add(request, 'add_user')

@api_view(['PUT'])
def replace_user(request, user_id):
    "Tries to update an user and returns the result"
    crud_object = Crud(UserSerializer, User, login_management.password_encode)
    return crud_object.replace(request, user_id, 'replace_user')

@api_view(['POST'])
def get_user(request, user_id):
    """Return a JSON response with user data for the given id"""
    crud_object = Crud(UserSerializer, User, login_management.password_hide)
    return crud_object.get(request, user_id, 'get_user')

@api_view(['DELETE'])
def delete_user(request, user_id):
    """Tries to delete an user and returns the result."""
    if user_management.check_current_user(request, user_id):
        crud_object = Crud(UserSerializer, User)
        return crud_object.delete(request, user_id, 'delete_user', "Usuario elminado exitosamente")
    return user_management.current_user_cannot_be_deleted_message()

@api_view(['POST'])
def toggle_user(request, user_id):
    """Toogles the active state for a given user"""
    crud_object = Crud(UserSerializer, User)
    return crud_object.toggle(request, user_id, 'toggle_user', "Usuario")

@api_view(['POST'])
def picker_search_user(request):
    """Returns a JSON response with user data for a selectpicker."""
    crud_object = Crud(BasicUserSerializer, User, data_filters.users_picker_filter)
    return crud_object.picker_search(request, 'picker_search_user')

@api_view(['POST'])
def list_user(request):
    """ Returns a JSON response containing registered users"""
    crud_object = Crud(BasicUserSerializer, User, data_filters.users_listing_filter)
    return crud_object.listing(request, 'list_user')

@api_view(['POST'])
def login(request):
    """Logs in the user if given credentials are valid"""
    data = login_management.login(request)
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

@api_view(['POST'])
def logout(request):
    """ Logs out the user from the system"""
    data = login_management.logout(request)
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

@api_view(['POST'])
def get_own(request):
    """Gets own user info"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_own')
    if validation['status']:
        user_obj = permission_obj.user
        user_serializer = UserSerializer(user_obj)
        user_data = user_serializer.data.copy()
        del user_data['password']

        data = {
            "success":True,
            "data":user_data
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

@api_view(['PUT'])
def replace_own(request):
    "Tries to update an user and returns the result"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('replace_own')
    if validation['status']:
        user_obj = permission_obj.user
        data = request.data.copy()
        password = data['password']
        confirm = data['confirm']
        data['profile'] = user_obj.profile.id
        del data['confirm']
        if password == "" and confirm == "":
            data['password'] = user_obj.password
        else:
            if password == confirm:
                data = login_management.password_encode(data)
            else:
                data['password'] = None
        user_serializer = UserSerializer(user_obj, data=data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"success":True},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )

        data = Crud.error_data(user_serializer)
        for i in range(0, len(data['Error']['details'])):
            if data['Error']['details'][i]['field'] == 'password':
                data['Error']['details'][i]['field'] = 'passwordConfirm'
                data['Error']['details'][i]['message'] = 'Las contraseñas no coinciden.'
                break
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)

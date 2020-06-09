"""Class for permission validation"""
import pytz
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from profiles.models import Profile, Action, ProfilePermissions
from .models import User, LoginSession

class PermissionValidation():
    """Class for permission validation"""
    def __init__(self, request):
        key = request.session.get('loginsession')
        if key is not None:
            login_session = LoginSession.objects.get(key=key)
        else:
            login_session = None
        self.login_session = login_session

    def validate(self, action_name):
        """Checks if the login_session has permissions to execute the action"""
        if self.login_session is None:
            return {
                'status': False,
                'error': 'Not logged'
            }

        timezone = pytz.timezone("America/Bogota")
        date_aware = timezone.localize(datetime.now())
  
        if self.login_session.life > date_aware:
            try:
                action = Action.objects.get(name=action_name)
                user = User.objects.get(id=self.login_session.user.id)
                profile = user.profile
                if self.action_possible(profile.id, action.id):
                    return {'status': True}
                else:
                    return {
                        'status': False,
                        'error': 'Forbidden'
                    }
            except:
                return {
                    'status': False,
                    'error': "Database error"
                }
        else:
            return {'status': False, 'error':'Not logged'}

    def logout(self, request):
        """Deletes the loginsession key to denout logout"""
        if self.login_session is not None:
            del request.session['loginsession']

    @staticmethod
    def action_possible(profile, action):
        """Fetch the profile permission and returns if it's possible"""
        try:
            permission = ProfilePermissions.objects.get(profile=profile, action=action)
            return permission.permission
        except:
            return False

    @staticmethod
    def error_response_webservice(validation, request):
        """Returns an error response depending on the validation"""
        if validation['error'] == 'Session expire':
            del request.session['loginsession']
            data = {
                "success": False,
                "message": "Su sessión expiro por favor ingrese nuevamente"
            }
            return Response(
                data,
                status=status.HTTP_401_UNAUTHORIZED,
                content_type='application/json')

        if validation['error'] == 'Not logged':
            data = {
                "success": False,
                "message": "Debe ingresar antes de realizar esta solicitud"
            }
            return Response(
                data,
                status=status.HTTP_401_UNAUTHORIZED,
                content_type='application/json')

        if validation['error'] == 'Forbidden':
            data = {
                "success": False,
                "message": "El usuario no tiene permisos para realizar esta acción"
            }
            return Response(
                data,
                status=status.HTTP_403_FORBIDDEN,
                content_type='application/json')

        if validation['error'] == 'Database error':
            data = {
                "success": False,
                "message": "El usuario, perfil o acción no se encontraron en la base de datos"
            }
            return Response(
                data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content_type='application/json')

        data = {
            "success": False,
            "message": "No se hay un mensaje para este error (" + validation['error'] + ")"
        }
        return Response(
            data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content_type='application/json')

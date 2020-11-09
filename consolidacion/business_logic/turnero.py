"""Contains functions for the turnero webservices"""
from datetime import datetime, timedelta, date
from rest_framework import status
from rest_framework.response import Response
from users.permission_validation import PermissionValidation
from sedes.models import Sede
from dms.models import TallCitas
from dms.serializers import TallCitasSerializer

def get_closest_turns(request):
    """Gets the turns that end after the current datetime for todays date"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_closest_turns')

    if validation['status']:
        data = request.data
        sede = data['sede']
        bodega = Sede.objects.get(pk=sede).bodega_dms
        criteria = {
            'estado_cita': 'P',
            'fecha_hora_fin__range': (datetime.now(), (date.today() + timedelta(seconds=186399))),
            'bodega': bodega
        }
        queryset = TallCitas.objects.filter(**criteria).order_by('-fecha_hora_ini')
        citas = TallCitasSerializer(queryset, many=True)
        answer = {
            'turnos': citas.data,
            'success': True
        }
        return Response(answer, status.HTTP_200_OK, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)
 
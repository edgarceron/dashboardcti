"""Containns crud extra operations for cosolidacion app"""
import csv
from rest_framework import status
from rest_framework.response import Response
from users.permission_validation import PermissionValidation
from agent_console.models import UserSede
from consolidacion.business_logic.list_class import ConsolidacionList
from consolidacion.serializers import ConsolidacionFileUploadsSerializer
from pprint import pprint

def add_sede_operation(request):
    """Return the data alter operation for add or replace crud standard"""
    permission_obj = PermissionValidation(request)
    user = permission_obj.user
    try:
        user_sede = UserSede.objects.get(user=user.id)
        sede = user_sede.sede
    except UserSede.DoesNotExist:
        sede = None
    def operation(data):
        if sede is not None:
            data['sede'] = sede.id
        else:
            data['sede'] = None
        return data
    return operation

def put_sede_motivo(request, queryset):
    """Puts the sede and motivo name to each object of the queryset"""
    consolidaciones = []
    for consolidacion in queryset:
        id = consolidacion.id
        cedula = consolidacion.cedula
        placa = consolidacion.placa
        fecha = consolidacion.fecha
        motivo = consolidacion.motivo.name
        if consolidacion.sede is None:
            sede = ""
            sede_id = 0
        else:
            sede = consolidacion.sede.name
            sede_id = consolidacion.sede.id
        if consolidacion.motivo is None:
            motivo = ""
            motivo_id = 0
        else:
            motivo = consolidacion.motivo.name
            motivo_id = consolidacion.motivo.id
        
        consolidaciones.append(
            ConsolidacionList(id, cedula, placa, fecha, motivo, sede, motivo_id, sede_id)
        )
    return consolidaciones

def upload_consolidacion(request):
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('upload_consolidacion')
    if validation['status']:
        pprint(request.data)
        file_serializer = ConsolidacionFileUploadsSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_name = file_serializer.data['file']
            with open(file_name, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    for col in row:
                        print(col)
            return Response(
                {"success":True, "message": "Archivo subido correctamente"},
                status=status.HTTP_201_CREATED,
                content_type='application/json'
            )
        return Response(
            {"success":False, "message": "Error al intentar guardar el archivo"},
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

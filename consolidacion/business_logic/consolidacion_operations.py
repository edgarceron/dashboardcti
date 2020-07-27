"""Containns crud extra operations for cosolidacion app"""
import csv
from rest_framework import status
from rest_framework.response import Response
from core.crud.standard import Crud
from users.permission_validation import PermissionValidation
from dms.models import Terceros
from agent_console.models import UserSede
from consolidacion.business_logic.list_class import ConsolidacionList
from consolidacion.serializers import ConsolidacionFileUploadsSerializer, ConsolidacionSerializer
from pprint import pprint

def validate_cedula(request):
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('validate_cedula')
    if validation['status']:
        data = request.data
        consolidacion_obj = ConsolidacionSerializer(data=data)
        if consolidacion_obj.is_valid():
            try:
                tercero = Terceros.objects.get(nit=data.cedula)
                return Response({
                    'success': True,
                    'nombre':tercero.nombres
                }, status.HTTP_200_OK, content_type='application/json')
            except Terceros.DoesNotExist:
                return Response(
                    {
                        'success': False,
                        'message':'No se encontro un cliente con esta cedula'
                    }, status.HTTP_200_OK, content_type='application/json')
        else:
            return Response(
                Crud.error_data(consolidacion_obj),
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json'
            )
    return permission_obj.error_response_webservice(validation, request)

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
            fails = []
            with open(file_name, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                line = 1
                error = False
                for row in spamreader:
                    aux = 1
                    data = {}
                    for col in row:
                        if aux == 1:
                            data['cedula'] = col
                        if aux == 2:
                            data['placa'] = col
                        if aux == 3:
                            data['fecha'] = col
                        if aux == 4:
                            data['motivo'] = col
                        if aux == 5:
                            data['sede'] = col
                        aux += 1

                    consolidacion = ConsolidacionSerializer(data=data)
                    if consolidacion.is_valid():
                        consolidacion.save()
                    else:
                        fails.append(';'.join(row))
                    aux = 1
                    line += 1
            return Response(
                {
                    "success":True,
                    "message": "Archivo subido correctamente",
                    "fails": fails
                },
                status=status.HTTP_201_CREATED,
                content_type='application/json'
            )
        return Response(
            {"success":False, "message": "Error al intentar guardar el archivo"},
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)


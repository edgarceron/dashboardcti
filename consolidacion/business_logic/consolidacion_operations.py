"""Containns crud extra operations for cosolidacion app"""
import csv
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from core.crud.standard import Crud
from users.permission_validation import PermissionValidation
from agent_console.models import UserSede
from dms.serializers import CrmCitasSerializer
from consolidacion.business_logic.list_class import ConsolidacionList
from consolidacion.serializers import ConsolidacionFileUploadsSerializer, ConsolidacionSerializer
from consolidacion.business_logic import citas

def validate_cedula(request):
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('validate_cedula')
    if validation['status']:
        data = request.data
        consolidacion_obj = ConsolidacionSerializer(data=data)
        if consolidacion_obj.is_valid():
            tercero = citas.get_tercero(data['cedula'])
            vehiculo = citas.get_veh(data['placa'])

            error_details = []
            if tercero is None:
                error_details.append({
                    "field": 'cedula',
                    "message": "No se encontro un cliente con esta cedula"
                })
            if vehiculo is None:
                error_details.append({
                    "field": 'placa',
                    "message": "No se encontro un vehiculo con esta placa"
                })
            if vehiculo is None or tercero is None:
                data = {
                    "Error": {
                        "success": False,
                        "status": 400,
                        "message": "Los datos enviados no son validos",
                        "details": error_details
                    }
                }
                return Response(
                    data,
                    status=status.HTTP_400_BAD_REQUEST,
                    content_type='application/json'
                )
            return Response({
                'success': True,
                'nombre':tercero.nombres
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
        id_consolidacion = consolidacion.id
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
            ConsolidacionList(id_consolidacion, cedula, placa, fecha, motivo, sede, motivo_id, sede_id)
        )
    return consolidaciones

def create_cf_observaciones_consolidacion(request, data_serializer):
    """Crea un registro en CF observaciones para indicar que se registro una
    consolidacio """
    data = request.data
    fecha = data['fecha']
    cedula = data['cedula']
    return insert_cf_observaciones(fecha, cedula)
    

def insert_cf_observaciones(fecha, cedula):
    """Creates a cf_observaciones in the database"""
    id_gru = 1
    id_sub = 19
    fecha_hora = datetime.now()
    hora = 0
    comentario = 'Llamada de consolidación creada Fecha: {}'.format(fecha)
    usuario = 'VOZIP'

    data = {
        'nit' : cedula,
        'id_gru' : id_gru,
        'id_sub' : id_sub,
        'fecha_hora' : fecha_hora,
        'hora' : hora,
        'comentario' : comentario,
        'usuario' : usuario
    }

    crm_cita = CrmCitasSerializer(data=data)
    if crm_cita.is_valid():
        crm_cita.save()
        return True
    print("Error al crear CF observaciones")
    return False

def upload_consolidacion(request):
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('upload_consolidacion')
    if validation['status']:
        file_serializer = ConsolidacionFileUploadsSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            file_name = file_serializer.data['file']
            fails = []
            with open(file_name, newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                line = 1
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
                        tercero = citas.get_tercero(data['cedula'])
                        vehiculo = citas.get_veh(data['placa'])
                        if tercero is None or vehiculo is None:
                            fails.append(';'.join(row))
                        else:
                            consolidacion.save()
                            insert_cf_observaciones(data['fecha'], data['cedula'])
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

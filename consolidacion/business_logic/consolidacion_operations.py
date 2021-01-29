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
from consolidacion.business_logic import citas, fail_management, show_results

def check_tercero_cedula(request):
    """Checks if the given nit belongs to a database tercero row and returns the name"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('check_tercero_cedula')
    if validation['status']:
        data = request.data
        nit = data['nit']
        tercero = citas.get_tercero(nit)
        answer = {}
        if tercero is None:
            answer['success'] = False
        else:
            answer['success'] = True
            answer['nombres'] = tercero.nombres
        return Response(answer, status.HTTP_200_OK, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)    

def check_placa(request):
    """Checks if the given placa belongs to a database vehicle"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('check_placa')
    if validation['status']:
        data = request.data
        placa = data['placa']
        vehiculo = citas.get_veh(placa)
        answer = {}
        if vehiculo is None:
            answer['success'] = False
        else:
            answer['success'] = True
        return Response(answer, status.HTTP_200_OK, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)        

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
    sede = get_user_sede(request)
    def operation(data):
        return data
    return operation

def get_user_sede(request):
    """Gets the sede of the current logged user"""
    permission_obj = PermissionValidation(request)
    user = permission_obj.user
    try:
        user_sede = UserSede.objects.get(user=user.id)
        sede = user_sede.sede
    except UserSede.DoesNotExist:
        sede = None
    return sede

def answer_not_user_sede():
    """Return an answer when user does not have a sede"""
    return Response({
        'success': False,
        'message':"""Error: Su usuario no esta asociado a una sede.
        Utilice la opción para subir datos por csv o contactese con
        el administrador"""
    }, status.HTTP_200_OK, content_type='application/json')

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
            ConsolidacionList(
                id_consolidacion, cedula, placa, fecha, motivo, sede, motivo_id, sede_id
            )
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

def fail_prepare(request):
    """Create new consolidations for failed consolidations in a given date range"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('fail_management')
    if validation['status']:
        data = request.data
        try:
            fail_management.prepare_to_call(data['start_date'], data['end_date'])
            success = True
            message = "Se volvera a llamar a las consolidaciones fallidas"
        except:
            success = False
            message = "Ocurrio un error al intentar crear las llamadas"
        return Response(
            {"success":success, "message": message},
            status=status.HTTP_400_BAD_REQUEST,
            content_type='application/json'
        )
    return permission_obj.error_response_webservice(validation, request)

def listing_citas_taller(request):
    """Lists tall_citas for a datatable"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_citas_taller')
    if validation['status']:
        sent_data = request.data
        draw = int(sent_data['draw'])
        start = int(sent_data['start'])
        length = int(sent_data['length'])
        agent = sent_data['agent']
        start_date = sent_data['start_date']
        end_date = sent_data['end_date']
        estado = sent_data['estado']
        sede = sent_data['sede']
        date_type = int(sent_data['date_type'])
        search = sent_data['search[value]']

        records_total = show_results.get_count_tall_citas()
        data, records_filtered = show_results.get_citas_manticore(
            agent, start_date, end_date, date_type, sede, estado, start, length, search)

        result = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data
        }
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)

def cancel_cita(request):
    """Cancels the cita_tall in DMS"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('cancel_cita')
    if validation['status']:
        data = request.data
        id_cita = data['id_cita']
        motivo = data['motivo']
        result = citas.cancel_cita(id_cita, motivo)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')
    return permission_obj.error_response_webservice(validation, request)

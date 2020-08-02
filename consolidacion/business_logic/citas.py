from rest_framework import status
from rest_framework.response import Response
from datetime import datetime, timedelta
from core.crud.standard import Crud
from users.permission_validation import PermissionValidation
from dms.models import Terceros, ReferenciasImp
from dms.serializers import CrmCitasSerializer, TallCitasSerializer
from consolidacion.models import CallConsolidacion
from sedes.models import Sede

# from consolidacion.business_logic import citas
# data = {'cedula':'1005783261', 'placa':'IPZ286','sede':1, 'motivo':'1', 'fecha':'2020-08-02','hora':'10:00'}
# tall_cita = citas.create_tall_cita(data)
# tall_cita.is_valid()
# tall_cita.errors
def create_cita(request):
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('validate_cedula')
    if validation['status']:
        data = {}
        tall_cita = create_tall_cita(request.data)

        if tall_cita.is_valid():
            data['tall_cita_data'] = tall_cita.data
        else:
            print(tall_cita.errors)
            data['tall_cita_data'] = tall_cita.errors

        crm_cita = create_crm_cita(tall_cita.data)

        if crm_cita.is_valid():
            data['crm_cita_data'] = crm_cita.data
        else:
            data['crm_cita_data'] = crm_cita.data

        if crm_cita.is_valid() and tall_cita.is_valid():
            crm_cita.save()
            tall_cita.save()
            update_call_consolidacion(request, tall_cita['id_cita'], crm_cita['seq'])
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

def update_call_consolidacion(request, tall_cita, crm_cita):
    id_cc = request.data['call_consolidacion_id']
    call_consolidacion = CallConsolidacion.objects.get(id=id_cc)
    call_consolidacion.cita_tall_id = tall_cita
    call_consolidacion.cita_crm_id = crm_cita
    call_consolidacion.save()

def create_crm_cita(tall_cita):
    nit_id = tall_cita['nit']
    id_gru = 3
    id_sub = 1
    fecha_hora = datetime.now()
    hora = 0
    comentario = 'Se realizo la cita para {} para el vechiculo de placas: {}'.format(
        tall_cita['fecha_hora_ini'],
        tall_cita['placa']
    )
    usuario = 'VOZIP'
    resultado = 0
    mail = tall_cita['mail']

    data = {
        'nit' : nit_id,
        'id_gru' : id_gru,
        'id_sub' : id_sub,
        'fecha_hora' : fecha_hora,
        'hora' : hora,
        'comentario' : comentario,
        'usuario' : usuario,
        'resultado' : resultado,
        'mail' : mail,
    }

    crm_cita = CrmCitasSerializer(data=data)
    return crm_cita

def create_tall_cita(data):
    tercero = get_tercero(data['cedula'])
    sede = get_sede(data['sede'])
    bodega = sede.bodega_dms
    fecha_hora_creacion = datetime.now()
    estado_cita = 'P'
    descripcion_estado = 'Programada'
    fecha_hora_ini, fecha_hora_fin = get_fecha_hora_cita(data['fecha'] + " " + data['hora'])
    hora = fecha_hora_ini.hour
    minutos = fecha_hora_ini.minute
    duracion_minutos = 15
    codigo_veh = get_veh(data['placa']).pk
    placa = data['placa']
    nit = int(data['cedula'])
    nombre_cliente = tercero.nombres
    nit_nuevo = 0
    nombre_encargado = sede.asesor.name
    telefonos = format_telefonos(tercero.telefono_1, tercero.telefono_2)
    notas = data['motivo']
    ano_veh = 0
    usuario = 'VOZIP'
    pc = 'DMSSERVER'
    modulo = ''
    mail = tercero.mail
    asesor = sede.asesor.name
    numerocomfrimaciones = 0
    numeroespacios = 0
    facturado = 'NA'

    data = {
        'bodega': bodega,
        'fecha_hora_creacion': fecha_hora_creacion,
        'estado_cita': estado_cita,
        #'descripcion_estado': descripcion_estado,
        'fecha_hora_ini': fecha_hora_ini,
        'fecha_hora_fin': fecha_hora_fin,
        'hora': hora,
        'minutos': minutos,
        'duracion_minutos': duracion_minutos,
        'codigo_veh': codigo_veh,
        'placa': placa,
        'nit': nit,
        'nombre_cliente': nombre_cliente,
        'nit_nuevo': nit_nuevo,
        'nombre_encargado': nombre_encargado,
        'telefonos': telefonos,
        'notas': notas,
        'ano_veh': ano_veh,
        'usuario': usuario,
        'pc': pc,
        'modulo': modulo,
        'mail': mail,
        'asesor': asesor,
        'numerocomfrimaciones': numerocomfrimaciones,
        'numeroespacios': numeroespacios,
        'facturado': facturado,
    }
    print(data)
    tall_cita = TallCitasSerializer(data=data)
    return tall_cita

def get_fecha_hora_cita(fecha_hora_string):
    fecha_hora_ini = datetime.strptime(fecha_hora_string, '%Y-%m-%d %H:%M')
    fecha_hora_fin = fecha_hora_ini + timedelta(minutes=15)
    return fecha_hora_ini, fecha_hora_fin

def get_tercero(cedula):
    try:
        return Terceros.objects.get(nit=cedula)
    except Terceros.DoesNotExist:
        return None

def get_sede(sede):
    return Sede.objects.get(id=sede)

def get_veh(placa):
    try:
        ref = ReferenciasImp.objects.get(placa=placa)
        return ref
    except ReferenciasImp.DoesNotExist:
        return None

def format_telefonos(tel1, tel2):
    if tel1 is None and tel2 is None:
        return ""
    elif tel2 is None:
        return tel1
    elif tel1 is None:
        return tel2
    else:
        return tel1 + "    " + tel2

"""Manages tall cita and crm cita operations"""
from django.db.models import Q
from datetime import datetime, timedelta
import pytz
from rest_framework import status
from rest_framework.response import Response
from core.mailing import mailing
from users.permission_validation import PermissionValidation
from agent_console.models import UserAgent, CallEntry
from dms.models import Terceros, ReferenciasImp, TallCitas, TallCitasOperaciones, TallCitasAuditoria
from dms.serializers import CrmCitasSerializer, TallCitasSerializer
from consolidacion.models import CallConsolidacion, CallEntryCita, CitaNoCall
from motivos.models import Motivo
from sedes.models import Sede
from asesores.models import Asesor

# from consolidacion.business_logic import citas
# data = {'cedula':'1005783261', 'placa':'IPZ286','sede':1, 'motivo':'1', 'fecha':'2020-08-02','hora':'10:00'}
# tall_cita = citas.create_tall_cita(data)
# tall_cita.is_valid()
# tall_cita.errors
def create_cita(request):
    data = {}
    permission_obj = PermissionValidation(request)
    id_user = permission_obj.user.id
    try:
        user_agent = UserAgent.objects.get(user=id_user)
        id_agent = user_agent.agent
    except UserAgent.DoesNotExist:
        id_agent = ""
        data["message"] = "Debe ser un agente para poder agendar citas"
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    tall_cita = create_tall_cita(request.data)

    if not tall_cita.is_valid():
        data['tall_cita_data'] = tall_cita.errors

    crm_cita = create_crm_cita(tall_cita.initial_data)

    if not crm_cita.is_valid():
        data['crm_cita_data'] = crm_cita.data

    if crm_cita.is_valid() and tall_cita.is_valid():
        model_crm = crm_cita.save()
        model_tall = tall_cita.save()
        data["tall_cita_id"] = model_tall.id_cita
        data["crm_cita_id"] = model_crm.seq
        update_call_consolidacion(request, model_tall.id_cita, model_crm.seq, id_agent)
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

def update_call_consolidacion(request, tall_cita, crm_cita, id_agent=""):
    """Updates a call_consolidacion when a call is registered to it"""
    id_cc = request.data['call_consolidacion_id']
    observaciones = request.data['observaciones']
    try:
        call_consolidacion = CallConsolidacion.objects.get(id=id_cc)
        call_consolidacion.cita_tall_id = tall_cita
        call_consolidacion.cita_crm_id = crm_cita
        call_consolidacion.observaciones = observaciones
        call_consolidacion.save()
    except CallConsolidacion.DoesNotExist:
        uniqueid_call_entry = request.data['id_call_entry']
        try:
            id_call_entry = CallEntry.objects.get(uniqueid=uniqueid_call_entry).id
        except CallEntry.DoesNotExist:
            id_call_entry = 0

        if id_call_entry != 0:
            call_entry_cita = CallEntryCita(
                cita_tall_id=tall_cita,
                cita_crm_id=crm_cita,
                call_entry=id_call_entry,
                observaciones=observaciones
            )
            call_entry_cita.save()
        else:
            cita_no_call = CitaNoCall(
                date=datetime.now(),
                cita_tall_id=tall_cita,
                cita_crm_id=crm_cita,
                agent=id_agent,
                observaciones=observaciones)
            cita_no_call.save()

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
    fecha_hora_ini, fecha_hora_fin = get_fecha_hora_cita(data['fecha'] + " " + data['hora'])
    hora = fecha_hora_ini.hour
    minutos = fecha_hora_ini.minute
    duracion_minutos = 15
    codigo_veh = get_veh(data['placa']).pk
    placa = data['placa']
    nit = int(data['cedula'])
    nombre_cliente = tercero.nombres
    nit_nuevo = 0
    nombre_encargado = get_asesor(data['asesor'])
    telefonos = format_telefonos(tercero.telefono_1, tercero.telefono_2)
    motivo = Motivo.objects.get(id=data['motivo'])
    notas = data['observaciones']  + " Motivo: " + motivo.name
    notas = notas[:400]
    ano_veh = 0
    usuario = 'VOZIP'
    pc = 'DMSSERVER'
    modulo = ''
    mail = tercero.mail
    asesor = get_asesor(data['asesor'])
    numerocomfrimaciones = 0
    numeroespacios = 0
    facturado = 'NA'

    data = {
        'bodega': bodega,
        'fecha_hora_creacion': fecha_hora_creacion,
        'estado_cita': estado_cita,
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
        'asesor': asesor[:20],
        'numerocomfrimaciones': numerocomfrimaciones,
        'numeroespacios': numeroespacios,
        'facturado': facturado,
    }
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

def get_asesor(asesor):
    return Asesor.objects.get(id=asesor).name

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

def citas_en_horario(sede, fecha, hora):
    """Shows citas in the given sede, date and time"""
    try: 
        sede = Sede.objects.get(pk=sede)
        bodega = sede.bodega_dms
        fecha_hora = fecha + " " + hora
        fecha = datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M')
        criteria = {
            'estado_cita': 'P',
            'fecha_hora_ini': fecha_hora,
            'bodega': bodega
        }

        tall_citas = TallCitas.objects.filter(**criteria)

        cita_ids = list(
            tall_citas.values_list('id_cita', flat=True)
        )

        citas_call = list(
            CallConsolidacion.objects.filter(cita_tall_id__in=cita_ids).values_list(
                'cita_tall_id', flat=True))

        citas_no_call = list(
            CitaNoCall.objects.filter(cita_tall_id__in=cita_ids).values_list(
                'cita_tall_id', flat=True))

        citas_call_entry = list(
            CallEntryCita.objects.filter(cita_tall_id=cita_ids).values_list(
                'cita_tall_id', flat=True))

        datetime_ocupados = tall_citas.filter(
            Q(id_cita__in=citas_call) | Q(id_cita__in=citas_no_call | Q(id_cita__in=citas_call_entry)))

        citas = TallCitasSerializer(datetime_ocupados, many=True)

        data = {
            'citas': citas.data
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    except Sede.DoesNotExist:
        data = {
            'message':"La sede solicitada no existe o fue borrada"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    except ValueError:
        data = {
            'message':"Proporcine una fecha y una sede adecuados para mostrar las citas en el horario"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

def verificar_horarios(sede, fecha):
    """Verifies avaible time for a date given a sede and a date"""
    try: 
        sede = Sede.objects.get(pk=sede)
        bodega = sede.bodega_dms
        fecha = datetime.strptime(fecha, '%Y-%m-%d')
        criteria = {
            'estado_cita': 'P',
            'fecha_hora_ini__range': (fecha, (fecha + timedelta(seconds=86399))),
            'bodega': bodega
        }

        tall_citas = TallCitas.objects.filter(**criteria)

        cita_ids = list(
            tall_citas.values_list('id_cita', flat=True)
        )

        citas_call = list(
            CallConsolidacion.objects.filter(cita_tall_id__in=cita_ids).values_list(
                'cita_tall_id', flat=True))

        citas_no_call = list(
            CitaNoCall.objects.filter(cita_tall_id__in=cita_ids).values_list(
                'cita_tall_id', flat=True))

        datetime_ocupados = list(
            tall_citas.filter(Q(id_cita__in=citas_call) | Q(id_cita__in=citas_no_call)).values_list(
                'fecha_hora_ini', flat=True))

        horarios_ocupados = []
        for x in datetime_ocupados:
            horarios_ocupados.append(x.strftime('%H:%M'))
        horarios_ocupados = set(horarios_ocupados)
        start = fecha.replace(hour = 7, minute=0)
        horarios = set({})

        while not (start.hour == 16 and start.minute == 00):
            horarios.add(start.strftime('%H:%M'))
            start += timedelta(minutes=15)

        #horarios = horarios.difference(horarios_ocupados)
        horarios = list(horarios)
        horarios.sort()
        data = {
            'horarios':horarios
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    except Sede.DoesNotExist:
        data = {
            'message':"La sede solicitada no existe o fue borrada"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    except ValueError:
        data = {
            'message':"Proporcine una fecha y una sede adecuados para mostrar horarios dispibles"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

def create_mail_and_send(data):
    """Creates the mail template and sends it"""
    tercero = get_tercero(data['cedula'])
    mail = tercero.mail
    if mail == "":
        return 0
    sede = get_sede(data['sede'])
    fecha_hora_creacion = datetime.now()
    placa = data['placa']
    telefonos = format_telefonos(tercero.telefono_1, tercero.telefono_2)
    motivo = Motivo.objects.get(id=data['motivo'])
    #mail = "maurinin@yahoo.com"
    asesor = get_asesor(data['asesor'])

    template = 'agent_console_mail/confirmacion.html'
    to = mail
    context = {
        'placa': placa,
        'asesor': asesor,
        'fecha': data['fecha'],
        'hora': data['hora'],
        'sede': sede.name,
        'direccion': sede.address,
        'motivo': motivo.name,
        'fecha_solicitud': fecha_hora_creacion,
        'nombre': tercero.nombres,
        'direccion_cliente': tercero.direccion,
        'correo': mail,
        'telefonos': telefonos
    }
    send_status = mailing.send_confirmacion(to, template, context)
    return {'status': send_status, 'mail': mail}

def datacita():
    context = {
        'placa': "ABC123",
        'asesor': "MAuro",
        'fecha': "2020-08-04",
        'hora': "10:00",
        'sede': "San Nicolas",
        'direccion': "Calle 62B",
        'motivo': "Mantenimi",
        'fecha_solicitud': datetime.now,
        'nombre': "Edgar",
        'direccion_cliente': "Calle 29",
        'correo': "maurinin@yahoo.com",
        'telefonos': "3176483290"
    }
    return context

def validate_cita(tall_cita):
    """Validates if tall_cita is cancelable"""
    message = ""
    succes = True

    timezone = pytz.timezone("America/Bogota")
    date_aware = timezone.localize(datetime.now())

    if tall_cita.estado_cita == 'C': 
        message = "La cita ya esta cancelada"
        succes = False
    return succes, message

def cancel_cita(id_cita, motivo):
    """Cancels the cita_tall in DMS"""
    result = {}
    try:
        tall_cita = TallCitas.objects.get(id_cita=id_cita)
        succes, message = validate_cita(tall_cita)
        if succes:
            tall_cita.estado_cita = 'C'
            tall_cita.save()
            operaciones = TallCitasOperaciones.objects.filter(id_cita=id_cita)
            for operacion in operaciones:
                operacion.delete()

            auditoria = TallCitasAuditoria(
                id_cita=tall_cita, usuario='IPRADA', pc='DMSSERVER',
                fecha_hora=datetime.now(),
                notas='Cita cancelada en manticore, motivo: ' + motivo)
            auditoria.save()
            result['success'] = succes
            result['message'] = "Cita cancelada con exito"
        else:
            result['success'] = succes
            result['message'] = message
    except TallCitas.DoesNotExist:
        result['success'] = False
        result['message'] = "La cita fue borrada del dms"
    return result

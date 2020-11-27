"""Contains functions for the turnero webservices"""
import pytz
from datetime import datetime, timedelta, date
from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response
from sedes.models import Sede
from dms.models import TallCitas
from agent_console.models import Calls
from consolidacion.models import CallConsolidacion, CitaNoCall

def get_closest_turns(sede):
    """Gets the turns that end after the current datetime for todays date"""
    collected_data = citas_hoy(sede)
    return Response(collected_data, status.HTTP_200_OK, content_type='application/json')

def citas_hoy(sede):
    """Gets citas tall info for csv by date"""
    sede = Sede.objects.get(id=sede)
    tall_cita_objects = tall_cita_date_range(sede.bodega_dms)
    id_citas = list(tall_cita_objects.values_list('id_cita', flat=True))

    calls_consolidacion = CallConsolidacion.objects.filter(cita_tall_id__in=id_citas)
    id_calls = list(calls_consolidacion.values_list('call', flat=True))
    criteria = {}
    criteria['id__in'] = id_calls
    calls = Calls.objects.filter(**criteria)
    id_calls = list(calls.values_list('id', flat=True))
    calls_consolidacion = calls_consolidacion.filter(call__in=id_calls)

    citas_no_call = CitaNoCall.objects.filter(cita_tall_id__in=id_citas)

    citas_tall = get_tall_citas_order(calls_consolidacion, citas_no_call)
    collected_data = get_tall_cita_row(citas_tall, [])
    return collected_data

def get_tall_citas_order(calls_consolidacion, citas_no_call):
    cita_tall_id_call = list(calls_consolidacion.values_list('cita_tall_id', flat=True))
    cita_tall_id_no_call = list(citas_no_call.values_list('cita_tall_id', flat=True))
    citas_tall = TallCitas.objects.filter(
        Q(id_cita__in=cita_tall_id_call) | Q(id_cita__in=cita_tall_id_no_call)).order_by('-fecha_hora_ini')
    return citas_tall

def tall_cita_date_range(bodega):
    """Gets the CitaNoCalls in the specified date range"""
    criteria = {}
    start_date = datetime.now()
    start_date = start_date.astimezone(pytz.timezone('America/Bogota'))
    start_date = datetime(start_date.year, start_date.month, start_date.day, start_date.hour, start_date.minute)

    end_date = datetime(date.today().year, date.today().month, date.today().day) + timedelta(seconds=86399)
    criteria['fecha_hora_ini__range'] = (start_date, end_date)
    criteria['bodega'] = bodega

    tall_cita_objects = TallCitas.objects.filter(**criteria)
    return tall_cita_objects

def put_data_cita(tall_cita):
    row = {}
    row['cedula'] = tall_cita.nit.nit
    row['placa'] = tall_cita.placa
    try:
        row['sede'] = Sede.objects.get(bodega_dms=tall_cita.bodega).name
    except Sede.DoesNotExist:
        row['sede'] = "Código de bodega dms" + tall_cita.bodega
    row['nombre_cliente'] = tall_cita.nombre_cliente
    row['nombre_encargado'] = tall_cita.nombre_encargado
    row['fecha_hora_ini'] = tall_cita.fecha_hora_ini
    row['telefonos'] = tall_cita.telefonos
    row['mail'] = tall_cita.mail
    row['observaciones'] = tall_cita.notas
    return row

def get_tall_cita_row(data, collected_data):
    """Gets a row for csv with TallCitas data"""
    for aux in data:
        row = put_data_cita(aux)
        collected_data.append(row)
    return collected_data

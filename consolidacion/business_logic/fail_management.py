from datetime import timedelta, datetime, date
from django.db.models import Q
from django.conf import settings
from dms.models import TallCitas
from agent_console.models import Calls
from consolidacion.models import CallConsolidacion, Consolidacion
from consolidacion.serializers import CallConsolidacionSerializer

def check_fails(start_date, end_date):
    consolidacion = calls_fail_date_range(start_date, end_date)
    data = []
    row = {}
    row['cedula'] = 'cedula'
    row['placa'] = 'placa'
    row['fecha'] = 'fecha'
    row['motivo'] = 'motivo'
    row['sede'] = 'sede'
    data.append(row)

    for x in consolidacion:
        row = {}
        row['cedula'] = x.cedula
        row['placa'] = x.placa
        row['fecha'] = x.fecha
        row['motivo'] = x.motivo
        row['sede'] = x.sede
        data.append(row)
    return data

def prepare_to_call(start_date, end_date):
    consolidacion = calls_fail_date_range(start_date, end_date)
    for x in consolidacion:
        old = x
        new = Consolidacion(
            cedula=old.cedula, placa=old.placa, fecha=date.today(), 
            motivo=old.motivo, sede=old.sede)
        new.save()

def calls_fail_date_range(start_date, end_date):
    """Gets ConsolidacionCalls in a date range"""
    criteria = {}

    if start_date != "" and end_date != "":
        start_date = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['fecha_llamada__range'] = (start_date, end_date)

    elif start_date != "":
        start_date = datetime.strptime(end_date, '%Y-%m-%d')
        criteria['fecha_llamada__gte'] = start_date

    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['fecha_llamada__lte'] = end_date

    calls = list(Calls.objects.values_list('id', flat=True).filter(
        Q(**criteria), Q(status='Abandoned') | Q(status='Failure') |
        Q(status='Placing') | Q(status='NoAsnwer')
    ))

    consolidaciones = Consolidacion.objects.filter(Q(callconsolidacion__call__in=calls))
    return consolidaciones

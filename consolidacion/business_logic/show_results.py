import csv
from datetime import timedelta, datetime
from django.conf import settings
from dms.models import TallCitas
from sedes.models import Sede
from agent_console.models import Calls
from consolidacion.models import CallConsolidacion, CitaNoCall

def data_to_csv(collected_data):
    """Transforms the collected data into a csv file a return"""
    csvfile = open(settings.STATIC_ROOT + 'result.csv', 'w')
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    for row in collected_data:
        writer.writerow(list(row.values()))
    return settings.STATIC_ROOT + 'result.csv'

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
    row['observaciones'] = str(tall_cita.notas).encode('cp1252').decode("utf-8")
    return row

def put_data_deleted():
    row = {}
    row['cedula'] = "Datos borrados del dms"
    row['placa'] = "Datos borrados del dms"
    row['sede'] = "Datos borrados del dms"
    row['nombre_cliente'] = "Datos borrados del dms"
    row['nombre_encargado'] = "Datos borrados del dms"
    row['fecha_hora_ini'] = "Datos borrados del dms"
    row['telefonos'] = "Datos borrados del dms"
    row['mail'] = "Datos borrados del dms"
    row['observaciones'] = "Datos borrados del dms"
    return row

def collect_data(agent="", start_date="", end_date=""):    
    calls_consolidacion = calls_date_range(agent, start_date, end_date)
    collected_data = []
    for aux in calls_consolidacion:
        try:
            tall_cita = TallCitas.objects.get(id_cita=aux.cita_tall_id)
            row = put_data_cita(tall_cita)
        except TallCitas.DoesNotExist:
            row = put_data_deleted()
        collected_data.append(row)
    citas_no_call = cita_no_call_date_range(agent, start_date, end_date)
    for aux in citas_no_call:
        try:
            tall_cita = TallCitas.objects.get(id_cita=aux.cita_tall_id)
            row = put_data_cita(tall_cita)
        except TallCitas.DoesNotExist:
            row = put_data_deleted()
        collected_data.append(row)
    return collected_data


def cita_no_call_date_range(agent, start_date, end_date):
    criteria = {}
    
    if start_date != "" and end_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['date__range'] = (start_date, end_date)

    elif start_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        criteria['date__gte'] = start_date

    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['date__lte'] = end_date

    if agent != "":
        criteria['agent'] = agent

    no_calls_consolidacion = CitaNoCall.objects.filter(**criteria)
    return no_calls_consolidacion

def calls_date_range(agent, start_date, end_date):

    criteria = {}

    if start_date != "" and end_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['datetime_entry_queue__range'] = (start_date, end_date)

    elif start_date != "":
        start_date = datetime.strptime(end_date, '%Y-%m-%d')
        criteria['datetime_entry_queue__gte'] = start_date

    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['datetime_entry_queue__lte'] = end_date
    
    if agent != "":
        criteria['id_agent'] = agent

    calls = list(Calls.objects.values_list('id', flat=True).filter(**criteria))

    calls_consolidacion = CallConsolidacion.objects.filter(call__in=calls)
    return calls_consolidacion

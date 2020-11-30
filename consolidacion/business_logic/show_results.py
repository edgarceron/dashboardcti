import csv
from datetime import timedelta, datetime
from django.conf import settings
from dms.models import TallCitas
from dms.serializers import TallCitasSerializer, TallCitasSerializerSimple
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
    row['observaciones'] = tall_cita.notas
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

def put_headers():
    row = {}
    row['cedula'] = "Cedula"
    row['placa'] = "Placa"
    row['sede'] = "Sede"
    row['nombre_cliente'] = "Nombre cliente"
    row['nombre_encargado'] = "Nombre asesor"
    row['fecha_hora_ini'] = "Fecha hora"
    row['telefonos'] = "Teléfonos"
    row['mail'] = "Correo"
    row['observaciones'] = "Observaciones"
    return row

def get_tall_cita_row(data, collected_data):
    """Gets a row for csv with TallCitas data"""
    for aux in data:
        try:
            tall_cita = TallCitas.objects.get(id_cita=aux.cita_tall_id)
            row = put_data_cita(tall_cita)
        except TallCitas.DoesNotExist:
            row = put_data_deleted()
        collected_data.append(row)
    return collected_data

def by_date_created(agent="", start_date="", end_date=""):
    """Gets citas tall info for csv by date created"""
    calls_consolidacion = calls_date_range(agent, start_date, end_date)
    collected_data = [put_headers()]
    collected_data = get_tall_cita_row(calls_consolidacion, [])
    citas_no_call = cita_no_call_date_range(agent, start_date, end_date)
    collected_data = get_tall_cita_row(citas_no_call, collected_data)
    return collected_data

def by_date_cita(agent="", start_date="", end_date=""):
    """Gets citas tall info for csv by date"""
    tall_cita_objects = tall_cita_date_range(start_date, end_date)
    id_citas = list(tall_cita_objects.values_list('id_cita', flat=True))

    calls_consolidacion = CallConsolidacion.objects.filter(cita_tall_id__in=id_citas)
    id_calls = list(calls_consolidacion.values_list('call', flat=True))
    criteria = {}
    if agent != "":
        criteria['id_agent'] = agent
    criteria['id__in'] = id_calls
    calls = Calls.objects.filter(**criteria)
    id_calls = list(calls.values_list('id', flat=True))
    calls_consolidacion = calls_consolidacion.filter(call__in=id_calls)
    collected_data = get_tall_cita_row(calls_consolidacion, [put_headers()])

    criteria = {}
    if agent != "":
        criteria['id_agent'] = agent
    criteria['cita_tall_id__in'] = id_citas
    citas_no_call = CitaNoCall.objects.filter(**criteria)
    collected_data = get_tall_cita_row(citas_no_call, collected_data)
    return collected_data

def tall_cita_date_range(start_date, end_date):
    """Gets the CitaNoCalls in the specified date range"""
    criteria = {}
    if start_date != "" and end_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['fecha_hora_ini__range'] = (start_date, end_date)

    elif start_date != "":
        start_date = datetime.strptime(end_date, '%Y-%m-%d')
        criteria['fecha_hora_ini__gte'] = start_date

    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['fecha_hora_ini__lte'] = end_date

    tall_cita_objects = TallCitas.objects.filter(**criteria)
    return tall_cita_objects

def collect_data(agent="", start_date="", end_date="", date_type=1):
    """Collects data from citas taller"""
    start_date = "" if start_date == "empty" else start_date
    end_date = "" if end_date == "empty" else end_date
    if date_type == 2:
        collected_data = by_date_created(agent, start_date, end_date)
    else:
        collected_data = by_date_cita(agent, start_date, end_date)
    return collected_data

def cita_no_call_date_range(agent, start_date, end_date):
    """Gets the CitaNoCalls in the specified date range for the specified agent"""
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
    """Gets the calls in the specified date range for the specified agent"""
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

    calls = list(Calls.objects.filter(**criteria).values_list('id', flat=True))

    calls_consolidacion = CallConsolidacion.objects.filter(call__in=calls)
    return calls_consolidacion

def get_citas_manticore(agent, start_date, end_date, date_type, start, length):
    """Gets the citas tall for a datatable"""
    if date_type == 2:
        citas_call = calls_date_range(
            agent, start_date, end_date
        ).values_list('cita_tall_id', flat=True)
        citas_no_call = cita_no_call_date_range(
            agent, start_date, end_date
        ).values_list('cita_tall_id', flat=True)
        citas_buscar = list(citas_no_call) + list(citas_call)
    
    else:
        tall_cita_objects = tall_cita_date_range(start_date, end_date)
        citas_id = list(tall_cita_objects.values_list('id_cita', flat=True))
        citas_call = CallConsolidacion.objects.filter(cita_tall_id__in=citas_id)
        id_calls = list(citas_call.values_list('call', flat=True))

        criteria = {}
        if agent != "":
            criteria['id_agent'] = agent
        criteria['id__in'] = id_calls

        calls = Calls.objects.filter(**criteria)
        id_calls = list(calls.values_list('id', flat=True))
        citas_call = list(citas_call.filter(
            call__in=id_calls
        ).values_list('cita_tall_id', flat=True))

        citas_no_call = list(
            cita_no_call_date_range(
                agent, "", ""
            ).filter(
                cita_tall_id__in=citas_id
            ).values_list('cita_tall_id', flat=True)
        )
        citas_buscar = citas_no_call + citas_call

    citas_taller = TallCitas.objects.filter(id_cita__in=citas_buscar)
    filtered = citas_taller[start:start + length]
    result = TallCitasSerializerSimple(filtered, many=True)
    data = result.data
    return data, citas_taller.count()

def get_count_tall_citas():
    return TallCitas.objects.count()

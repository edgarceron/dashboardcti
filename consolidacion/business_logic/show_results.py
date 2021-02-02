import csv
from datetime import timedelta, datetime
from django.conf import settings
from dms.models import TallCitas
from dms.serializers import TallCitasSerializer, TallCitasSerializerSimple
from sedes.models import Sede
from agent_console.models import Calls, CallEntry
from consolidacion.models import CallConsolidacion, CitaNoCall, CallEntryCita
from django.db.models import Q

def data_to_csv(collected_data, header=True):
    """Transforms the collected data into a csv file a return"""
    csvfile = open(settings.STATIC_ROOT + 'result.csv', 'w')
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    if header:
        writer.writerow(put_headers())
    for row in collected_data:
        writer.writerow(to_dict(row))
    return settings.STATIC_ROOT + 'result.csv'

def to_dict(row):
    return dict(list(row.items())).values()

def get_observaciones(id_cita):
    try:
        observaciones = CallConsolidacion.objects.get(cita_tall_id=id_cita).observaciones
    except CallConsolidacion.DoesNotExist:
        try:
            observaciones = CallEntryCita.objects.get(cita_tall_id=id_cita).observaciones
        except CallEntryCita.DoesNotExist:
            try:
                observaciones = CitaNoCall.objects.get(cita_tall_id=id_cita).observaciones
            except CitaNoCall.DoesNotExist:
                observaciones = ""
    return observaciones

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
    row['estado'] = tall_cita.estado_cita
    row['observaciones'] = get_observaciones(tall_cita.id_cita).replace('\n'," ")
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
    row['estado'] = "Datos borrados del dms"
    row['observaciones'] = "Datos borrados del dms"
    return row

def put_headers():
    row = {}
    row['id_cita'] = "ID Cita"
    row['bodega'] = "Sede"
    row['fecha_hora_ini'] = "Fecha y hora"
    row['placa'] = "Placa"
    row['nit'] = "Nit"
    row['nombre_cliente'] = "Nombre cliente"
    row['nombre_encargado'] = "Nombre encargado"
    row['telefonos'] = "Telefonos"
    row['notas'] = "Observaciones"
    row['mail'] = "Correo"
    row['asesor'] = "Asesor"
    row['estado_cita'] = "Estado cita"
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

def tall_cita_date_range(start_date, end_date):
    """Gets the CitaNoCalls in the specified date range"""
    criteria = {}
    if start_date != "" and end_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['fecha_hora_ini__range'] = (start_date, end_date)

    elif start_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        criteria['fecha_hora_ini__gte'] = start_date

    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['fecha_hora_ini__lte'] = end_date

    tall_cita_objects = TallCitas.objects.filter(**criteria)
    return tall_cita_objects

def collect_data(agent="", start_date="", end_date="", date_type=1, sede="", estado=""):
    """Collects data from citas taller"""
    start_date = "" if start_date == "empty" else start_date
    end_date = "" if end_date == "empty" else end_date
    estado = "" if estado == "empty" else estado
    sede = "" if sede == 0 else sede
    collected_data, count = get_citas_manticore(
        agent, start_date, end_date, date_type, sede, estado, "", "")
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
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        criteria['datetime_entry_queue__gte'] = start_date

    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['datetime_entry_queue__lte'] = end_date

    if agent != "":
        criteria['id_agent'] = agent

    calls = list(Calls.objects.filter(**criteria).values_list('id', flat=True))

    calls_consolidacion = CallConsolidacion.objects.filter(call__in=calls)
    return calls_consolidacion

def call_entry_date_range(agent, start_date, end_date):
    """Gets the calls in the specified date range for the specified agent"""
    criteria = {}

    if start_date != "" and end_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['datetime_entry_queue__range'] = (start_date, end_date)

    elif start_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        criteria['datetime_entry_queue__gte'] = start_date

    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        criteria['datetime_entry_queue__lte'] = end_date

    if agent != "":
        criteria['id_agent'] = agent

    calls = list(CallEntry.objects.filter(**criteria).values_list('id', flat=True))

    call_entry_consolidacion = CallEntryCita.objects.filter(call_entry__in=calls)
    return call_entry_consolidacion

def filter_citas_tall(agent, start_date, end_date):
    tall_cita_objects = tall_cita_date_range(start_date, end_date)
    citas_id = list(tall_cita_objects.values_list('id_cita', flat=True))
    citas_call = CallConsolidacion.objects.filter(cita_tall_id__in=citas_id)
    id_calls = list(citas_call.values_list('call', flat=True))
    citas_call_entry = CallEntryCita.objects.filter(cita_tall_id__in=citas_id)
    ids_call_entry = list(citas_call_entry.values_list('call_entry', flat=True))

    criteria = {}
    if agent != "":
        criteria['id_agent'] = agent
    criteria['id__in'] = id_calls

    calls = Calls.objects.filter(**criteria)
    id_calls = list(calls.values_list('id', flat=True))
    citas_call_ids = list(citas_call.filter(
        call__in=id_calls
    ).values_list('cita_tall_id', flat=True))

    criteria = {}
    if agent != "":
        criteria['id_agent'] = agent
    criteria['id__in'] = ids_call_entry

    call_entry = CallEntry.objects.filter(**criteria)
    ids_call_entry = list(call_entry.values_list('id', flat=True))
    citas_call_entry_ids = list(citas_call_entry.filter(
        call_entry__in=ids_call_entry
    ).values_list('cita_tall_id', flat=True))


    citas_no_call_ids = list(
        cita_no_call_date_range(
            agent, "", ""
        ).filter(
            cita_tall_id__in=citas_id
        ).values_list('cita_tall_id', flat=True)
    )
    citas_buscar = citas_no_call_ids + citas_call_ids + citas_call_entry_ids
    return citas_buscar

def get_citas_manticore(agent, start_date, end_date, date_type, sede, estado, start, length, search=""):
    """Gets the citas tall for a datatable"""
    if date_type == 2:
        citas_call = calls_date_range(
            agent, start_date, end_date
        ).values_list('cita_tall_id', flat=True)
        citas_call_entry = call_entry_date_range(
            agent, start_date, end_date
        ).values_list('cita_tall_id', flat=True)
        citas_no_call = cita_no_call_date_range(
            agent, start_date, end_date
        ).values_list('cita_tall_id', flat=True)
        citas_buscar = list(citas_no_call) + list(citas_call) + list(citas_call_entry)

    else:
        citas_buscar = filter_citas_tall(agent, start_date, end_date)

    criteria = {}
    criteria["id_cita__in"] = citas_buscar

    bodega = get_bodega(sede)
    if bodega != "":
        criteria['bodega'] = bodega

    if estado != "":
        criteria['estado_cita'] = estado

    citas_taller = TallCitas.objects.filter(**criteria)

    if search != "":
        citas_taller = citas_taller.filter(
            Q(nombre_cliente__icontains=search) |
            Q(nombre_encargado__icontains=search) |
            Q(asesor__icontains=search) |
            Q(telefonos__icontains=search) |
            Q(mail__icontains=search) |
            Q(placa__icontains=search) |
            Q(nit__nit__icontains=search) 
        )
    if start != "":
        filtered = citas_taller[start:start + length]
    else:
        filtered = citas_taller
    result = TallCitasSerializerSimple(filtered, many=True)
    
    data = result.data
    return data, citas_taller.count()

def get_bodega(sede):
    """Gets the bodega_dms fot the given sede"""
    try:
        sede = Sede.objects.get(id=int(sede))
        return sede.bodega_dms
    except Sede.DoesNotExist:
        return ""
    except ValueError:
        return ""

def get_count_tall_citas():
    """Gets count call of tall citas"""
    return TallCitas.objects.count()

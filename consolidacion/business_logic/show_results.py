import csv
from datetime import timedelta, datetime
from django.conf import settings
from dms.models import TallCitas
from agent_console.models import Calls
from consolidacion.models import CallConsolidacion

def data_to_csv(collected_data):
    """Transforms the collected data into a csv file a return"""
    csvfile = open(settings.STATIC_ROOT + 'result.csv', 'w')
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator = '\n')
    for row in collected_data:
        writer.writerow(list(row.values()))
    return settings.STATIC_ROOT + 'result.csv'

def collect_data(agent="", start_date="", end_date=""):    
    calls_consolidacion = calls_date_range(agent, start_date, end_date)
    collected_data = []
    for aux in calls_consolidacion:
        row['cedula'] = aux.consolidacion.cedula
        row['placa'] = aux.consolidacion.placa
        row['sede'] =aux.consolidacion.sede
        row['observaciones'] = aux.observaciones
        try:
            row = {}
            tall_cita = TallCitas.objects.get(id=aux.cita_tall_id) 
            row['nombre_cliente'] = tall_cita.nombre_cliente
            row['nombre_encargado'] = tall_cita.nombre_encargado
            row['fecha_hora_ini'] = tall_cita.fecha_hora_ini
            row['telefonos'] = tall_cita.telefonos
            row['mail'] = tall_cita.mail
            row['observaciones'] = aux.observaciones   
        except TallCitas.DoesNotExist:
            row['nombre_cliente'] = "Datos borrados del dms"
            row['nombre_encargado'] = "Datos borrados del dms"
            row['fecha_hora_ini'] = "Datos borrados del dms"
            row['telefonos'] = "Datos borrados del dms"
            row['mail'] = "Datos borrados del dms"
        collected_data.append(row)
    return collected_data


def calls_date_range(agent, start_date, end_date):

    criteria = {}

    if start_date != "" and end_date != "":
        start_date = datetime.strptime(end_date, '%Y-%m-%d')
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

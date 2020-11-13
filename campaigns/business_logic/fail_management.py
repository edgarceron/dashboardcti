from django.db.models import Q, Count
from datetime import timedelta, datetime, date
from agent_console.models import Calls
from campaigns.models import CampaignForm, AnswersHeader


def check_fails(campaign, start_date, end_date):
    """Returns the data of failed poll calls"""
    campaign_isabel = CampaignForm.objects.get(id=campaign).isabel_campaign
    headers_fail = headers_fail_date_range(campaign_isabel, start_date, end_date)
    data = []
    row = {}
    row['cedula'] = 'cedula'
    row['placa'] = 'placa'
    row['nombre'] = 'nombre'
    row['telefono'] = 'telefono'
    row['correo'] = 'correo'
    row['linea_vehiculo'] = 'linea_vehiculo'
    data.append(row)

    for header_info in headers_fail:
        row = {}
        row['cedula'] = header_info.data_llamada.cedula
        row['placa'] = header_info.data_llamada.placa
        row['nombre'] = header_info.data_llamada.name
        row['telefono'] = header_info.data_llamada.telefono
        row['correo'] = header_info.data_llamada.correo
        row['linea_vehiculo'] = header_info.data_llamada.linea_veh
        data.append(row)
    return data

def prepare_to_call(campaign, start_date, end_date):
    """Creates new headers for the failed calls in the given date range for the given campaign"""
    campaign_isabel = CampaignForm.objects.get(id=campaign).isabel_campaign
    headers_fail = headers_fail_date_range(campaign_isabel, start_date, end_date)
    for old in headers_fail:
        try:
            old_call = Calls.objects.get(id=old.call_id)
            new_call = Calls(
                phone=old_call.phone, id_campaign=old_call.id_campaign,
                retries=0, dnc=0, scheduled=0)
            new_call.save()
        except Calls.DoesNotExist:
            old_data = old.data_llamada
            new_call = Calls(
                phone=old_data.telefono, id_campaign=campaign_isabel,
                retries=0, dnc=0, scheduled=0)

        new = AnswersHeader(
            campaign=campaign, tercero=old.tercero, agente=None,
            call_id=new_call, data_llamada=old.data_llamada)
        new.save()

def headers_fail_date_range(campaign, start_date, end_date):
    """Gets ConsolidacionCalls in a date range"""
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

    if campaign != "":
        criteria['id_campaign'] = campaign

    calls = list(Calls.objects.values_list('id', flat=True).filter(
        Q(**criteria), Q(status='Abandoned') | Q(status='Failure') |
        Q(status='Placing') | Q(status='NoAsnwer')
    ))
    
    headers = AnswersHeader.objects.annotate(
        number_of_bodies=Count('answersbody')
    ).filter(
        Q(call_id__in=calls) |
        Q(number_of_bodies=0))
    return headers

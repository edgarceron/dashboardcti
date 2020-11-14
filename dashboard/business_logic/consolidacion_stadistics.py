from datetime import timedelta, datetime
from consolidacion.models import CallConsolidacion, CallEntryCita
from agent_console.models import CallEntry, Calls, AgentConsoleOptions, Agent

SALIENTE = 1
ENTRANTE = 2

def consolidacion_count(start_date, end_date, agent):
    option_campaign = AgentConsoleOptions.objects.get(option='CAMPAIGN_CONSOLIDACION')

    criteria = {}
    criteria['id_campaign'] = option_campaign.value
    if agent != "":
        criteria['id_agent'] = agent

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

    calls = list(Calls.objects.values_list('id', flat=True).filter(**criteria))

    count = CallConsolidacion.objects.filter(call__in=calls).count()
    return count

def cita_count(start_date, end_date, agent, campaign):
    call_entry_citas = list(
        CallEntryCita.objects.values_list('call_entry', flat=True).all())

    criteria = {}
    if agent != '':
        criteria['id_agent'] = agent

    if campaign != '':
        criteria['id_campaign'] = campaign

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

    criteria['id__in'] = call_entry_citas

    count = CallEntry.objects.filter(**criteria).count()
    return count

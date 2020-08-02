"""Functions for calls by status counting"""
from django.db.models import Count 
from agent_console.models import Calls, CallEntry, CurrentCallEntry, CurrentCalls

def count_calls(start_date, end_date, agent, queue):
    """Counts row from Calls by status"""
    query_calls_by_status = list(
        Calls.objects.all().values('status').annotate(total=Count('status'))
    )
    calls_by_status = {}
    total = 0
    for obj in query_calls_by_status:
        calls_by_status[obj['status']] = obj['total']
        total = total + obj['total']

    calls_by_status['total'] = total

    if not 'Abandoned' in calls_by_status:
        calls_by_status['Abandoned'] = 0
    if not 'Failure' in calls_by_status:
        calls_by_status['Failure'] = 0
    if not 'Placing' in calls_by_status:
        calls_by_status['Placing'] = 0
    if not 'ShortCall' in calls_by_status:
        calls_by_status['ShortCall'] = 0
    if not 'Success' in calls_by_status:
        calls_by_status['Success'] = 0
    
    return calls_by_status

def count_call_entry(start_date, end_date, agent, queue):
    """Counts row from CallEntry by status"""
    conditions = {}
    if (start_date != "" and end_date != ""):
        conditions['datetime_entry_queue__range'] = (start_date, end_date)
    elif start_date != "":
        conditions['datetime_entry_queue__gte'] = start_date
    elif end_date != "":
        conditions['datetime_entry_queue__lte'] = start_date

    if agent != "":
        conditions['agent'] = agent

    if queue != "":
        conditions['queue'] = queue

    query_call_entry_by_status = list(
        CallEntry.objects.filter(
            conditions
        ).values('status').annotate(total=Count('status'))
    )
    call_entry_by_status = {}

    total = 0
    for obj in query_call_entry_by_status:
        call_entry_by_status[obj['status']] = obj['total']
        total = total + obj['total']

    call_entry_by_status['total'] = total

    if not 'terminada' in call_entry_by_status:
        call_entry_by_status['terminada'] = 0
    if not 'abandonada' in call_entry_by_status:
        call_entry_by_status['abandonada'] = 0
    if not 'en-cola' in call_entry_by_status:
        call_entry_by_status['en-cola'] = 0
    if not 'activa' in call_entry_by_status:
        call_entry_by_status['activa'] = 0

    return call_entry_by_status

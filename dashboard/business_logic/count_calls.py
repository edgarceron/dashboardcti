"""Functions for calls by status counting"""
from datetime import timedelta
from django.db.models import Count 
from agent_console.models import Calls, CallEntry, CurrentCallEntry, CurrentCalls

def count_calls(start_date, end_date, agent, campaign):
    """Counts row from Calls by status"""
    conditions = {}
    if (start_date != "" and end_date != ""):
        conditions['start_time__range'] = (start_date, end_date  + timedelta(seconds=86399))
    elif start_date != "":
        conditions['start_time__gte'] = start_date
    elif end_date != "":
        conditions['start_time__lte'] = start_date

    if agent != "":
        conditions['id_agent'] = agent

    if campaign != "":
        conditions['id_campaign'] = campaign

    query_calls_by_status = list(
        Calls.objects.filter(
            conditions
        ).values('status').annotate(total=Count('status'))
    )
    calls_by_status = {}
    total = 0
    for obj in query_calls_by_status:
        calls_by_status[obj['status']] = obj['total']
        total = total + obj['total']

    calls_by_status['total'] = total

    if 'Abandoned' not in calls_by_status:
        calls_by_status['Abandoned'] = 0
    if 'Failure' not in calls_by_status:
        calls_by_status['Failure'] = 0
    if 'Placing' not in calls_by_status:
        calls_by_status['Placing'] = 0
    if 'ShortCall' not in calls_by_status:
        calls_by_status['ShortCall'] = 0
    if 'Success' not in calls_by_status:
        calls_by_status['Success'] = 0
    if None not in calls_by_status:
        calls_by_status[None] = 0

    return calls_by_status

def count_call_entry(start_date, end_date, agent, campaign):
    """Counts row from CallEntry by status"""
    conditions = {}
    if (start_date != "" and end_date != ""):
        conditions['datetime_entry_queue__range'] = (start_date, end_date  + timedelta(seconds=86399))
    elif start_date != "":
        conditions['datetime_entry_queue__gte'] = start_date
    elif end_date != "":
        conditions['datetime_entry_queue__lte'] = start_date

    if agent != "":
        conditions['agent'] = agent

    if campaign != "":
        conditions['id_campaign'] = campaign

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

    if 'terminada' not in call_entry_by_status:
        call_entry_by_status['terminada'] = 0
    if 'abandonada' not in call_entry_by_status:
        call_entry_by_status['abandonada'] = 0
    if 'en-cola' not in call_entry_by_status:
        call_entry_by_status['en-cola'] = 0

    return call_entry_by_status

def count_current_calls():
    """Returns the number of active calls"""
    current_calls = {}
    current_calls['outgoing'] = CurrentCalls.objects.all().count()
    current_calls['incoming'] = CurrentCallEntry.objects.all().count()
    return current_calls

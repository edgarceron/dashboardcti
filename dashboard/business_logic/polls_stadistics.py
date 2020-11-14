from datetime import timedelta, datetime
from campaigns.models import CampaignForm, AnswersHeader
from agent_console.models import Calls, CallEntry

SALIENTE = 1
ENTRANTE = 2

def polls_attended(start_date, end_date, agent, campaign, type_campaign):
    """Gets the total polls attended given a criteria"""
    total = 0
    criteria = {}
    if type_campaign == SALIENTE:
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

        criteria = {}
        criteria['call_id__in'] = calls
        criteria['campaign__type_campaign'] = type_campaign
        if campaign != "":
            criteria['campaign__isabel_campaign'] = campaign

    else:
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

        calls = list(CallEntry.objects.values_list('id', flat=True).filter(**criteria))

        criteria = {}
        criteria['call_id__in'] = calls
        criteria['campaign__type_campaign'] = type_campaign
        if campaign != "":
            criteria['campaign__isabel_campaign'] = campaign

    total = AnswersHeader.objects.filter(**criteria).count()
    return total

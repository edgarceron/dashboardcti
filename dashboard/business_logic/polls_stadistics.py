from datetime import timedelta, datetime
from campaigns.models import CampaignForm, AnswersHeader
from agent_console.models import Calls, CallEntry

SALIENTE = 1
ENTRANTE = 2

def polls_attended(start_date, end_date, agent, campaign, type_campaign):
    """Gets the total polls attended given a criteria"""
    total = 0

    criteria = {}

    criteria['type_campaign'] = type_campaign
    if campaign != "":
        criteria['isabel_campaign'] = campaign

    campaign_manticore = list(CampaignForm.objects.values_list('id', flat=True).filter(**criteria))

    criteria = {}
    if campaign != "":
        criteria['campaign__in'] = campaign_manticore
    if agent != "":
        criteria['agent'] = agent

    criteria['campaign__type_campaign'] = type_campaign
    id_calls = list(AnswersHeader.objects.values_list('call_id', flat=True).filter(**criteria))

    calls = []

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

        criteria['id__in'] = id_calls

        calls = list(Calls.objects.values_list('id', flat=True).filter(**criteria))
        total = AnswersHeader.objects.filter(call_id__in=calls).count()
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

        criteria['id__in'] = id_calls


        calls = list(CallEntry.objects.values_list('id', flat=True).filter(**criteria))
        total = AnswersHeader.objects.filter(call_id__in=calls).count()

    return total

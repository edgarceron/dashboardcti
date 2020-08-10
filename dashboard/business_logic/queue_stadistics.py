"""Contains functions to calculate stadistics about queue calls"""
from django.db.models import Avg
from agent_console.models import CallEntry, CampaignEntry, Agent
from agent_console.serializers import CurrentCallEntrySerializer
from dashboard.business_logic import criteria_conditions

def get_longest_wait_queue_call(campaign):
    """Gets the active call with the longest wait"""
    conditions = {}

    if campaign != "":
        queue = CampaignEntry.objects.get(pk=campaign).queue
        conditions['queue'] = queue

    conditions['status'] = 'en-cola'

    queue_calls = list(
        CallEntry.objects.filter(
            **conditions
        ).order_by("datetime_entry_queue")
    )

    if len(queue_calls) > 0:
        longest_wait_queue_call = queue_calls[0]
    else:
        longest_wait_queue_call = None

    return CurrentCallEntrySerializer(longest_wait_queue_call).data

def get_average_wait(start_date, end_date, agent, campaign):
    """Gets the average wait-in-queue time"""
    conditions = criteria_conditions.get_call_criteria(
        start_date, end_date, agent, campaign
    )

    query_avg = CallEntry.objects.filter(
        **conditions
    ).aggregate(Avg('duration_wait'))

    average_wait = query_avg['duration_wait__avg']
    return average_wait

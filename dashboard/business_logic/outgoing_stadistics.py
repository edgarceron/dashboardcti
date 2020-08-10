"""Manages stadistics of outgoing calls times"""
from django.db.models import Avg
from agent_console.models import Calls
from agent_console.serializers import CallsSerializer
from dashboard.business_logic import criteria_conditions

def get_average_duration(start_date, end_date, agent, campaign):
    """Calculates the average duration of outgoing calls given a criteria"""
    conditions = criteria_conditions.get_call_criteria(
        start_date, end_date, agent, campaign
    )

    query_avg = Calls.objects.filter(
        **conditions
    ).aggregate(Avg('duration'))

    average_duration = query_avg['duration__avg']
    return average_duration

def get_longest_outgoing_call(start_date, end_date, agent, campaign):
    conditions = criteria_conditions.get_call_criteria(
        start_date, end_date, agent, campaign
    )

    duration_query = list(
        Calls.objects.filter(
            **conditions
        ).order_by("-duration")
    )

    if len(duration_query) > 0:
        longest_outgoing_call = duration_query[0]
    else:
        longest_outgoing_call = None

    return CallsSerializer(longest_outgoing_call).data

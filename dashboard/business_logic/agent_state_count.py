"""Manages function to count how many agents are in each state"""
from agent_console.models import Audit, CurrentCallEntry, CurrentCalls

def get_agents_logged():
    """Returns the numbre of agents logued"""
    query = Audit.objects.filter(
        id_break__isnull=True,
        datetime_end__isnull=True
    )
    agents = query.values_list('id_agent', flat=True)
    count = query.count()
    return count, agents

def get_agents_in_break(agents_logged):
    """Returns the number of agents in break"""
    query = Audit.objects.filter(
        id_agent__in=agents_logged,
        id_break__isnull=False,
        datetime_end__isnull=True
    )
    #agents_break = query.values_list('id_agent', 'id_break', 'datetime_init')
    count = query.count()
    return count

def get_agents_in_call(campaign=None):
    """Return the number of agents attending a call"""
    conditions = {}
    if campaign is not None and campaign != "":
        conditions['id_call__id_campaign'] = campaign
    queryout = CurrentCalls.objects.filter(**conditions)

    conditions = {}
    if campaign is not None and campaign != "":
        conditions['id_call_entry__id_campaign'] = campaign
    queryentry = CurrentCallEntry.objects.filter(**conditions)
    return queryout.count() + queryentry.count()

"""Contains fuctions to give TMO or service level stadistics"""
from agent_console.models import CallEntry, AgentConsoleOptions
from dashboard.business_logic import criteria_conditions

def get_answered_before(start_date, end_date, agent, campaign):
    """Counts and return the calls answered before n seconds, n
    taken from the TMOTIME option in AgentConsole table"""
    try:
        seconds = AgentConsoleOptions.objects.get(option='TMOTIME').value
    except AgentConsoleOptions.DoesNotExist:
        seconds = 30

    conditions = criteria_conditions.get_call_criteria(
        start_date, end_date, agent, campaign
    )
    conditions['duration_wait__lte'] = seconds

    answered_before = CallEntry.objects.filter(
        **conditions
    ).count()

    return answered_before, seconds

def get_service_level(before, total):
    """Computes service level"""
    if total > 0:
        service_level = before/total * 100
    else:
        service_level = 100
    return "%.2f" % service_level

def get_tmo(before, answered):
    """Computes TMO"""
    if answered > 0:
        tmo = before/answered * 100
    else:
        tmo = 100
    return "%.2f" % tmo

def get_effectiveness(success, total):
    """Computes effectiveness level"""
    if total > 0:
        effectiveness = success/total * 100
    else:
        effectiveness = 100
    return "%.2f" % effectiveness

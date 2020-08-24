"""Looks for calls maded in call center db that are not registeres in default"""
from consolidacion.models import CallConsolidacion
from agent_console.models import Calls, AgentConsoleOptions, Campaign

def set_made_calls():
    """Sets CallConsolidacion made field to true is the call has been made"""
    check = CallConsolidacion.objects.filter(call_made=False)
    retries = get_retries_consolidacion_campaing()
    call_consolidations = list(check.values_list('call', flat=True))
    set_not_dialied_consolidacion_state(call_consolidations, retries)
    for call_consolidacion in check:
        call = Calls.objects.get(id=call_consolidacion.call)
        if (call.status != "Placing" and call.status is not None) or call.retries >= retries:
            call_consolidacion.call_made = True
            call_consolidacion.save()

def set_not_dialied_consolidacion_state(call_consolidations, retries):
    """
    Sets incorrectly dialed calls status to Failure.
    A Call is incorrectly dialed if its status is null and an above
    call has a not null status.
    """
    today_consolidacion = Calls.objects.filter(id__in=call_consolidations, status__isnull=True)
    for call in today_consolidacion:
        id_call = call.id
        done_after = Calls.objects.filter(id__gte=id_call, status__isnull=False).count()
        if done_after:
            call.status = 'Failure'
            call.retries = retries
            call.save()

def get_retries_consolidacion_campaing():
    """Return the numbre of retries setter for the consolidación campaign"""
    id_campaign = AgentConsoleOptions.objects.get(option='CAMPAIGN_CONSOLIDACION').value
    retries = Campaign.objects.get(id=id_campaign)
    return retries

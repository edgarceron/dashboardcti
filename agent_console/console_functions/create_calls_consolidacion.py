from django.db.models import Q
from consolidacion.models import Consolidacion, CallConsolidacion
from agent_console.models import Calls, AgentConsoleOptions, Campaign
from dms.models import Terceros

def create_calls_consolidacion():
    """Create the consolidación calls in the campaign"""
    to_create = Consolidacion.objects.filter(callconsolidacion=None)
    cedulas = to_create.values_list('cedula', flat=True)
    phones = get_phones(cedulas)
    campaign = get_campaign()
    for consolidacion in to_create:
        cedula = consolidacion.cedula
        call = Calls(phone=phones[cedula][0], id_campaign=campaign)
        call.save()
        call_consolidacion = CallConsolidacion(consolidacion, call)
        call_consolidacion.save()

    campaign_obj = Campaign.objects.filter(id=campaign)
    campaign_obj.estatus = 'A'
    campaign_obj.save()


def get_failed_calls():
    ids_calls = CallConsolidacion.objects.values_list('call', flat=True)
    calls_fail = Calls.objects.filter(id__in=ids_calls, status='Failure')
    calls_fail = calls_fail.values_list('id', flat=True)
    return calls_fail

def get_campaign():
    """Gets the campaign of consolidacion calls"""
    option_campaign = AgentConsoleOptions.objects.get(option="CAMPAIGN_CONSOLIDACION")
    id_campaign = option_campaign.value
    return id_campaign

def get_phones(cedulas):
    """Get the phones for the consolidacion calls"""
    numbers = Terceros.objects.filter(nit__in=cedulas)
    numbers = numbers.values_list('nit', 'telefono_1', 'telefono_2', flat=True)
    phones = {}
    for x in range (0, len(numbers)):
        phones[numbers[x][0]] = numbers[1:2]
    return phones

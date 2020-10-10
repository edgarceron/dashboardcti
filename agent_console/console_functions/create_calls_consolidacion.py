from datetime import datetime, timedelta
from consolidacion.serializers import CallConsolidacionSerializer
from consolidacion.models import Consolidacion, CallConsolidacion
from agent_console.models import Calls, AgentConsoleOptions, Campaign
from agent_console.serializers import CallsSerializer
from dms.models import Terceros

def create_calls_consolidacion():
    """Create the consolidación calls in the campaign"""
    to_create = Consolidacion.objects.filter(
        callconsolidacion=None,
        fecha__lte=(datetime.today() + timedelta(seconds=86399))
    )
    cedulas = list(to_create.values_list('cedula', flat=True))
    phones = get_phones(cedulas)
    pk_campaign = get_campaign()
    try:
        campaign_obj = Campaign.objects.get(id=pk_campaign)
        for consolidacion in to_create:
            cedula = consolidacion.cedula
            data = {
                'phone': phones[cedula][0],
                'id_campaign': pk_campaign,
                'retries': 0,
                'dnc': 0,
                'scheduled': 0
            }
            call = CallsSerializer(data=data)
            if call.is_valid():
                call.save()
                print("Llamada creada")
                data_cc = {
                    'consolidacion': consolidacion.id,
                    'call': call.data['id']
                }
                call_consolidacion = CallConsolidacionSerializer(data=data_cc)
                if call_consolidacion.is_valid():
                    call_consolidacion.save()
                else:
                    print(call_consolidacion.errors)
                    print('Error')
            else:
                print(call.errors)
                print('Error')

        campaign_obj.estatus = 'A'
        campaign_obj.save()

    except Campaign.DoesNotExist:
        print("La campaña no existe o fue borrada")


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
    numbers = numbers.values_list('nit', 'telefono_1', 'telefono_2')
    phones = {}
    for x in range (0, len(numbers)):
        phones[str(numbers[x][0]).strip()] = [str(numbers[x][1]).strip(), str(numbers[x][2]).strip()]
        #phones[str(numbers[x][0])] = ['3176483290']
    return phones

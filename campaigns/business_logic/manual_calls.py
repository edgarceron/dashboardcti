"""Manages operations to save manual calls"""
from datetime import datetime
from agent_console.models import Calls, Campaign, Agent
from campaigns.models import DataLlamada, CampaignForm

def create_call(data : dict):
    call_id = data.get('call_id')
    if call_id is None:
        data_llamada = DataLlamada.objects.get(pk=data.get("data_llamada"))
        campaign_form = CampaignForm.objects.get(pk=data.get("campaign"))
        new_call = Calls()
        new_call.id_campaign = Campaign(campaign_form.isabel_campaign)
        new_call.phone = data_llamada.telefono
        new_call.agent = Agent(data.get('agent'))
        new_call.retries = 0
        new_call.status = "Success"
        new_call.fecha_llamada = datetime.now()
        new_call.start_time = datetime.now()
        new_call.end_time = datetime.now()
        new_call.duration = 0
        new_call.dnc = 0
        new_call.date_init = datetime.date()
        new_call.date_end = datetime.date()
        new_call.time_init = datetime.now()
        new_call.time_end = datetime.now()
        new_call.scheduled = 0
        try: 
            new_call.save()
            return True
        except Exception as e:
            return False

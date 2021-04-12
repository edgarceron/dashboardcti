"""Manages operations to save manual calls"""
from datetime import datetime
from campaigns.models import AnswersHeader
from agent_console.models import Calls, Campaign, Agent
from campaigns.models import DataLlamada, CampaignForm


def create_call(request, answer_header_id):
    answer_header = AnswersHeader.objects.get(answer_header_id)
    if answer_header.call_id is None:
        request_data = request.data.copy()
        data_llamada = DataLlamada.objects.get(pk=request_data.get("data_llamada"))
        campaign_form = CampaignForm.objects.get(pk=request_data.get("campaign"))
        new_call = Calls()
        new_call.id_campaign = Campaign(campaign_form.isabel_campaign)
        new_call.phone = data_llamada.telefono
        new_call.agent = Agent(request_data.get('agent'))
        new_call.retries = 0
        new_call.status = "Success"
        new_call.fecha_llamada = datetime.now()
        new_call.start_time = datetime.now()
        new_call.end_time = datetime.now()
        new_call.duration = 0
        new_call.dnc = 0
        new_call.date_init = datetime.today()
        new_call.date_end = datetime.today()
        new_call.time_init = datetime.now()
        new_call.time_end = datetime.now()
        new_call.datetime_entry_queue = datetime.today()
        new_call.scheduled = 0
        new_call.save()
        answer_header.call_id = new_call.id
        answer_header.campaign = campaign_form
        answer_header.data_llamada = data_llamada
        answer_header.save()

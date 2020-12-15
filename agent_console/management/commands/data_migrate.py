"""Migrates data to a sql file from a elastix or isabel server"""
from django.db.models import Q
from django.core.management.base import BaseCommand
from agent_console.models import Agent, Campaign, CampaignEntry, Calls, CallEntry, QueueCallEntry
from consolidacion.models import CallConsolidacion, CallEntryCita
from campaigns.models import AnswersHeader

class Command(BaseCommand):
    """Creates the calls for the consolidación modules"""
    def handle(self, *args, **options):
        agents = sql_agents() + ";\n\n"
        camp = sql_campaign() + ";\n\n"
        calls = sql_calls() + ";\n\n"
        entry = sql_campaign_entry() + ";\n\n"
        queue = sql_queue_call_entry() + ";\n\n"
        call_entry = sql_call_entry() + ";\n\n"

        f = open("migration.sql", "a")
        f.write(agents)
        f.write(camp)
        f.write(calls)
        f.write(entry)
        f.write(queue)
        f.write(call_entry)
        f.close()

def sql_agents():
    list_agents = Agent.objects.all()
    sql = "INSERT INTO agent (id, type, number, name, password, estatus, eccp_password) VALUES "
    for agent in list_agents:
        sql += "\n ("
        sql += agent.id + ", "
        sql += agent.type + ", "
        sql += agent.number + ", "
        sql += agent.name + ", "
        sql += agent.password + ", "
        sql += agent.estatus + ", "
        sql += agent.eccp_password + ", "
        sql += "),"
    sql = sql[:-1]
    return sql

def sql_campaign():
    list_campaign = Campaign.objects.all()
    sql = """INSERT INTO campaign (id, name, datetime_init, datetime_end, daytime_init, 
        daytime_end, retries, trunk, context, queue, max_canales, num_completadas, 
        promedio, desviacion, script, estatus, id_url)"""
    for camp in list_campaign:
        sql += "\n ("
        sql += camp.id + ", "
        sql += camp.name + ", "
        sql += camp.datetime_init + ", "
        sql += camp.datetime_end + ", "
        sql += camp.daytime_init + ", "
        sql += camp.daytime_end + ", "
        sql += camp.retries + ", "
        sql += camp.trunk + ", "
        sql += camp.context + ", "
        sql += camp.queue + ", "
        sql += camp.max_canales + ", "
        sql += camp.num_completadas + ", "
        sql += camp.promedio + ", "
        sql += camp.desviacion + ", "
        sql += camp.script + ", "
        sql += camp.estatus + ", "
        sql += camp.id_url + ", "
        sql += "),"
    sql = sql[:-1]
    return sql

def sql_calls():
    cita_call = list(CallConsolidacion.objects.all().values_list('call', flat=True))
    poll_call = list( 
        AnswersHeader.objects.filter(campaign__type_campaign=1).values_list('call_id',flat=True)
    )
    filtered = Calls.objects.filter(Q(id__in=cita_call) | Q(id__in=poll_call))
    sql = """INSERT INTO calls (id, id_campaign, phone, status, uniqueid, fecha_llamada, 
        start_time, end_time, retries, duration, id_agent, transfer, datetime_entry_queue, 
        duration_wait, dnc, date_init, date_end, time_init, time_end, agent, failure_cause, 
        failure_cause_txt, datetime_originate, trunk, scheduled)"""
    for call in filtered:
        sql += "\n ("
        sql += call.id + ", "
        sql += call.id_campaign + ", "
        sql += call.phone + ", "
        sql += call.status + ", "
        sql += call.uniqueid + ", "
        sql += call.fecha_llamada + ", "
        sql += call.start_time + ", "
        sql += call.end_time + ", "
        sql += call.retries + ", "
        sql += call.duration + ", "
        sql += call.id_agent + ", "
        sql += call.transfer + ", "
        sql += call.datetime_entry_queue + ", "
        sql += call.duration_wait + ", "
        sql += call.dnc + ", "
        sql += call.date_init + ", "
        sql += call.date_end + ", "
        sql += call.time_init + ", "
        sql += call.time_end + ", "
        sql += call.agent + ", "
        sql += call.failure_cause + ", "
        sql += call.failure_cause_txt + ", "
        sql += call.datetime_originate + ", "
        sql += call.trunk + ", "
        sql += call.scheduled + ", "
        sql += "),"
    sql = sql[:-1]
    return sql

def sql_campaign_entry():
    campaings = CampaignEntry.objects.all()
    sql = """INSERT INTO campaign_entry (id, name, id_queue_call_entry, id_form, 
        datetime_init, datetime_end, daytime_init, daytime_end, estatus, script, id_url)
        VALUES """
    
    for camp in campaings:
        sql += "\n ("
        sql += camp.id + ", "
        sql += camp.name + ", "
        sql += camp.id_queue_call_entry + ", "
        sql += camp.id_form + ", "
        sql += camp.datetime_init + ", "
        sql += camp.datetime_end + ", "
        sql += camp.daytime_init + ", "
        sql += camp.daytime_end + ", "
        sql += camp.estatus + ", "
        sql += camp.script + ", "
        sql += camp.id_url + ", "
        sql += "),"
    sql = sql[:-1]
    return sql

def sql_call_entry():
    cita_calls = list(CallEntryCita.objects.all().values_list('call_entry', flat=True))
    poll_call = list( 
        AnswersHeader.objects.filter(campaign__type_campaign=2).values_list('call_id',flat=True)
    )
    calls = CallEntry.objects.filter(Q(id__in=cita_calls) | Q(id_in=poll_call))
    sql = """INSERT INTO call_entry (id, id_agent, id_queue_call_entry, id_contact, 
        callerid, datetime_init, datetime_end, duration, status, transfer, 
        datetime_entry_queue, duration_wait, uniqueid, id_campaign, trunk)"""

    for entry in calls:
        sql += "\n ("
        sql += entry.id + ", "
        sql += entry.id_agent + ", "
        sql += entry.id_queue_call_entry + ", "
        sql += entry.id_contact + ", "
        sql += entry.callerid + ", "
        sql += entry.datetime_init + ", "
        sql += entry.datetime_end + ", "
        sql += entry.duration + ", "
        sql += entry.status + ", "
        sql += entry.transfer + ", "
        sql += entry.datetime_entry_queue + ", "
        sql += entry.duration_wait + ", "
        sql += entry.uniqueid + ", "
        sql += entry.id_campaign + ", "
        sql += entry.trunk + ", "
        sql += "),"
    sql = sql[:-1]
    return sql

def sql_queue_call_entry():
    queues = QueueCallEntry.objects.all()
    sql = """INSERT INTO query_call_entry (id, queue, date_init, time_init, 
        date_end, time_end, estatus, script) VALUES """
    for queue in queues:
        sql += "\n ("
        sql += queue.id + ", "
        sql += queue.queue + ", "
        sql += queue.date_init + ", "
        sql += queue.time_init + ", "
        sql += queue.date_end + ", "
        sql += queue.time_end + ", "
        sql += queue.estatus + ", "
        sql += queue.script + ", "
        sql += "),"
    sql = sql[:-1]
    return sql
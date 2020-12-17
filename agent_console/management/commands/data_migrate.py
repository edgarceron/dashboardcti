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
        sql += str(agent.id) + ", "
        sql += "'" + str(agent.type) + "', "
        sql += "'" + str(agent.number) + "', "
        sql += "'" + str(agent.name) + "', "
        sql += "'" + str(agent.password) + "', "
        sql += "'" + str(agent.estatus) + "', "
        sql += "'" + str(agent.eccp_password) + "'"
        sql += "),"
    sql = sql[:-1]
    sql = sql.replace('None', 'NULL')
    sql = sql.replace('\'NULL\'', 'NULL')
    return sql

def sql_campaign():
    list_campaign = Campaign.objects.all()
    sql = """INSERT INTO campaign (id, name, datetime_init, datetime_end, daytime_init, 
        daytime_end, retries, trunk, context, queue, max_canales, num_completadas, 
        promedio, desviacion, script, estatus, id_url) VALUES """
    for camp in list_campaign:
        sql += "\n ("
        sql += str(camp.id) + ", "
        sql += "'" + str(camp.name) + "', "
        sql += "'" + str(camp.datetime_init) + "', "
        sql += "'" + str(camp.datetime_end) + "', "
        sql += "'" + str(camp.daytime_init) + "', "
        sql += "'" + str(camp.daytime_end) + "', "
        sql += str(camp.retries) + ", "
        sql += "'" + str(camp.trunk) + "', "
        sql += "'" + str(camp.context) + "', "
        sql += "'" + str(camp.queue) + "', "
        sql += str(camp.max_canales) + ", "
        sql += str(camp.num_completadas) + ", "
        sql += str(camp.promedio) + ", "
        sql += str(camp.desviacion) + ", "
        sql += "'<p></p>', "
        sql += "'" + str(camp.estatus) + "', "
        sql += str(camp.id_url)
        sql += "),"
    sql = sql[:-1]
    sql = sql.replace('None', 'NULL')
    sql = sql.replace('\'NULL\'', 'NULL')
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
        failure_cause_txt, datetime_originate, trunk, scheduled) VALUES """
    for call in filtered:
        sql += "\n ("
        sql += str(call.id) + ", "
        sql += "'" + str(call.id_campaign.id) + "', "
        sql += "'" + str(call.phone) + "', "
        sql += "'" + str(call.status) + "', "
        sql += "'" + str(call.uniqueid) + "', "
        sql += "'" + str(call.fecha_llamada) + "', "
        sql += "'" + str(call.start_time) + "', "
        sql += "'" + str(call.end_time) + "', "
        sql += str(call.retries) + ", "
        sql += str(call.duration) + ", "
        if(call.id_agent != None):
            sql += str(call.id_agent.id) + ", "
        else:
            sql += "NULL, "
        sql += "'" + str(call.transfer) + "', "
        sql += "'" + str(call.datetime_entry_queue) + "', "
        sql += str(call.duration_wait) + ", "
        sql += str(call.dnc) + ", "
        sql += "'" + str(call.date_init) + "', "
        sql += "'" + str(call.date_end) + "', "
        sql += "'" + str(call.time_init) + "', "
        sql += "'" + str(call.time_end) + "', "
        sql += str(call.agent) + ", "
        sql += str(call.failure_cause) + ", "
        sql += "'" + str(call.failure_cause_txt) + "', "
        sql += "'" + str(call.datetime_originate) + "', "
        sql += "'" + str(call.trunk) + "', "
        sql += str(call.scheduled)
        sql += "),"
    sql = sql[:-1]
    sql = sql.replace('None', 'NULL')
    sql = sql.replace('\'NULL\'', 'NULL')
    return sql

def sql_campaign_entry():
    campaings = CampaignEntry.objects.all()
    sql = """INSERT INTO campaign_entry (id, name, id_queue_call_entry, id_form, 
        datetime_init, datetime_end, daytime_init, daytime_end, estatus, script, id_url)
        VALUES """
    
    for camp in campaings:
        sql += "\n ("
        sql += str(camp.id) + ", "
        sql += "'" + str(camp.name) + "', "
        sql += str(camp.id_queue_call_entry.id) + ", "
        sql += str(camp.id_form) + ", "
        sql += "'" + str(camp.datetime_init) + "', "
        sql += "'" + str(camp.datetime_end) + "', "
        sql += "'" + str(camp.daytime_init) + "', "
        sql += "'" + str(camp.daytime_end) + "', "
        sql += "'" + str(camp.estatus) + "', "
        sql += "'<p></p>', "
        sql += str(camp.id_url)
        sql += "),"
    sql = sql[:-1]
    sql = sql.replace('None', 'NULL')
    sql = sql.replace('\'NULL\'', 'NULL')
    return sql

def sql_call_entry():
    cita_calls = list(CallEntryCita.objects.all().values_list('call_entry', flat=True))
    poll_call = list( 
        AnswersHeader.objects.filter(campaign__type_campaign=2).values_list('call_id',flat=True)
    )
    calls = CallEntry.objects.filter(Q(id__in=cita_calls) | Q(id__in=poll_call))
    sql = """INSERT INTO call_entry (id, id_agent, id_queue_call_entry, id_contact, 
        callerid, datetime_init, datetime_end, duration, status, transfer, 
        datetime_entry_queue, duration_wait, uniqueid, id_campaign, trunk) VALUES"""

    for entry in calls:
        sql += "\n ("
        sql += str(entry.id) + ", "
        sql += str(entry.id_agent.id) + ", "
        sql += str(entry.id_queue_call_entry.id) + ", "
        sql += str(entry.id_contact) + ", "
        sql += "'" + str(entry.callerid) + "', "
        sql += "'" + str(entry.datetime_init) + "', "
        sql += "'" + str(entry.datetime_end) + "', "
        sql += str(entry.duration) + ", "
        sql += "'" + str(entry.status) + "', "
        if entry.transfer is None:
            sql += "NULL, "
        else:
            sql += "'" + str(entry.transfer) + "', "
        sql += "'" + str(entry.datetime_entry_queue) + "', "
        sql += str(entry.duration_wait) + ", "
        sql += "'" + str(entry.uniqueid) + "', "
        sql += str(entry.id_campaign.id) + ", "
        sql += "'" + str(entry.trunk) + "'"
        sql += "),"
    sql = sql[:-1]
    sql = sql.replace('None', 'NULL')
    sql = sql.replace('\'NULL\'', 'NULL')
    return sql

def sql_queue_call_entry():
    queues = QueueCallEntry.objects.all()
    sql = """INSERT INTO queue_call_entry (id, queue, date_init, time_init, 
        date_end, time_end, estatus, script) VALUES """
    for queue in queues:
        sql += "\n ("
        sql += "'" + str(queue.id) + "', "
        sql += "'" + str(queue.queue) + "', "
        sql += "'" + str(queue.date_init) + "', "
        sql += "'" + str(queue.time_init) + "', "
        sql += "'" + str(queue.date_end) + "', "
        sql += "'" + str(queue.time_end) + "', "
        sql += "'" + str(queue.estatus) + "', "
        sql += "'<p></p>'"
        sql += "),"
    sql = sql[:-1]
    sql = sql.replace('None', 'NULL')
    sql = sql.replace('\'NULL\'', 'NULL')
    return sql

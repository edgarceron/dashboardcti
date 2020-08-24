"""Counts calls per hour"""
from django.db import connections

def get_call_entry_per_hour(start_date, end_date, agent, campaign):
    """Counts the call entry per hour in a date range with the given agent and/or campaign"""
    if (start_date != "" and end_date != ""):
        condition_fecha = 'datetime_entry_queue BETWEEN "' + start_date
        condition_fecha += '" AND DATE_ADD("' + end_date + '", INTERVAL 86399 SECOND)'
    elif start_date != "":
        condition_fecha = 'datetime_entry_queue >= "' + start_date + '"'
    elif end_date != "":
        condition_fecha = 'datetime_entry_queue <= "' + end_date + '"'
    else:
        condition_fecha = 'datetime_entry_queue >= CURDATE()'

    conditions_agent = ""
    conditions_campaign = ""
    if agent != "":
        conditions_agent = ' AND id_agent = ' + agent

    if campaign != "":
        conditions_campaign = ' AND id_campaign = ' + campaign

    query_base = """SELECT HOUR(datetime_entry_queue) AS hr, COUNT(DISTINCT(id)) as
        cuenta FROM call_entry WHERE """
    query_base += condition_fecha + conditions_agent + conditions_campaign
    query_all = query_base + ' AND (status="abandonada" or status="terminada") GROUP BY hr'
    query_abandonadas = query_base + ' AND (status="abandonada") GROUP BY hr'
    query_terminadas = query_base + ' AND (status="terminada") GROUP BY hr'

    cursor = connections['call_center'].cursor()
    cursor.execute(query_all)
    result_all = cursor.fetchall()

    cursor.execute(query_abandonadas)
    result_abandonadas = cursor.fetchall()

    cursor.execute(query_terminadas)
    result_terminadas = cursor.fetchall()

    calls_per_hour = {}
    calls_abandonadas = {}
    call_terminadas = {}
    for hour in range(0, 24):
        calls_per_hour[hour] = 0
        calls_abandonadas[hour] = 0
        call_terminadas[hour] = 0

    calls_per_hour = hour_replace(result_all, calls_per_hour)
    calls_abandonadas = hour_replace(result_abandonadas, calls_abandonadas)
    call_terminadas = hour_replace(result_terminadas, call_terminadas)

    return {
        'calls_per_hour': calls_per_hour,
        'calls_abandonadas': calls_abandonadas,
        'call_terminadas': call_terminadas,
    }

def get_calls_per_hour(start_date, end_date, agent, campaign):
    """Counts the calls per hour in a date range with the given agent and/or campaign"""
    if (start_date != "" and end_date != ""):
        condition_fecha = 'datetime_originate BETWEEN "' + start_date
        condition_fecha += '" AND DATE_ADD("' + end_date + '", INTERVAL 86399 SECOND)'
    elif start_date != "":
        condition_fecha = 'datetime_originate >= "' + start_date + '"'
    elif end_date != "":
        condition_fecha = 'datetime_originate <= "' + end_date + '"'
    else:
        condition_fecha = 'datetime_originate >= CURDATE()'

    conditions_agent = ""
    conditions_campaign = ""
    if agent != "":
        conditions_agent = ' AND id_agent = ' + agent

    if campaign != "":
        conditions_campaign = ' AND id_campaign = ' + campaign

    query_base = """SELECT HOUR(datetime_originate) AS hr, COUNT(DISTINCT(id)) as
        cuenta FROM calls WHERE """
    query_base += condition_fecha + conditions_agent + conditions_campaign
    query_all = query_base + ' GROUP BY hr'
    query_abandonadas = query_base + """ AND ((status="Abandoned")
    OR (status="Failure") OR (status="ShortCall") OR (status="NoAnswer")) GROUP BY hr"""
    query_terminadas = query_base + ' AND (status="Success") GROUP BY hr'
    query_pendientes = query_base + ' AND ((status is NULL) OR (status="Placing")) GROUP BY hr'

    cursor = connections['call_center'].cursor()
    cursor.execute(query_all)
    result_all = cursor.fetchall()

    cursor.execute(query_abandonadas)
    result_abandonadas = cursor.fetchall()

    cursor.execute(query_terminadas)
    result_terminadas = cursor.fetchall()

    cursor.execute(query_pendientes)
    result_pendientes = cursor.fetchall()

    calls_per_hour = {}
    calls_abandonadas = {}
    calls_terminadas = {}
    calls_pendientes = {}
    for hour in range(0, 24):
        calls_per_hour[hour] = 0
        calls_abandonadas[hour] = 0
        calls_terminadas[hour] = 0
        calls_pendientes[hour] = 0

    calls_per_hour = hour_replace(result_all, calls_per_hour)
    calls_abandonadas = hour_replace(result_abandonadas, calls_abandonadas)
    calls_terminadas = hour_replace(result_terminadas, calls_terminadas)
    calls_pendientes = hour_replace(result_pendientes, calls_pendientes)

    return {
        'calls_per_hour': calls_per_hour,
        'calls_abandonadas': calls_abandonadas,
        'calls_terminadas': calls_terminadas,
        'calls_pendientes': calls_pendientes,
    }

def hour_replace(result, hours):
    """Fills hours with the result rows"""
    for row in result:
        hours[row[0]] = row[1]

    hours_list = []
    for x in range(0,24):
        hours_list.append(hours[x])

    return hours_list

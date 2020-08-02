from django.db import connections

def get_calls_per_hour(start_date, end_date, agent, queue):
    """Counts the calls per hout in a date range with the given agent and/or queue"""
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
    conditions_queue = ""
    if agent != "":
        conditions_agent = ' AND id_agent = ' + agent

    if queue != "":
        conditions_queue = ' AND id_queue' + queue

    query_base = """SELECT HOUR(datetime_entry_queue) AS hr, COUNT(DISTINCT(id)) as
        cuenta FROM call_entry WHERE """
    query_base += condition_fecha + conditions_agent + conditions_queue
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

    calls_per_hour, calls_abandonadas, call_terminadas = {}
    for hour in range(0, 23):
        calls_per_hour[hour] = 0
        calls_abandonadas[hour] = 0
        call_terminadas[hour] = 0

    calls_per_hour = hour_replace(result_all, calls_per_hour)
    calls_abandonadas = hour_replace(result_abandonadas, calls_abandonadas)
    call_terminadas = hour_replace(result_terminadas, call_terminadas)

    return calls_per_hour, calls_abandonadas, call_terminadas

def hour_replace(result, hours):
    """Fills hours with the result rows"""
    for row in result:
        hours[row[0]] = row[1]
    return hours

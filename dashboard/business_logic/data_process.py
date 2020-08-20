"""Data procesing for dashboard requests"""
from dashboard.business_logic import queue_stadistics, tmo_calls, agent_state_count
from dashboard.business_logic import calls_per_hour, count_calls, outgoing_stadistics
def data_outgoing(request):
    """Calls functions to get dashboard data"""
    data = request.data
    id_agent = data['id_agent']
    id_campaign = data['id_campaign']
    start_date = data['start_date']
    end_date = data['end_date']

    calls_out_per_hour = calls_per_hour.get_calls_per_hour(
        start_date,
        end_date,
        id_campaign,
        id_agent
    )

    calls_count = count_calls.count_calls(start_date, end_date, id_agent, id_campaign)

    average_outgoing_duration = outgoing_stadistics.get_average_duration(
        start_date, end_date, id_agent, id_campaign
    )

    longets_outgoing_call = outgoing_stadistics.get_longest_outgoing_call(
        start_date, end_date, id_agent, id_campaign
    )

    response = {
        'calls_out_per_hour': calls_out_per_hour,
        'calls_count': calls_count,
        'average_outgoing_duration': average_outgoing_duration,
        'longets_outgoing_call': longets_outgoing_call
    }

    return response

def data_entry(request):
    data = request.data
    id_agent = data['id_agent']
    id_campaign = data['id_campaign']
    start_date = data['start_date']
    end_date = data['end_date']

    call_entry_per_hour = calls_per_hour.get_call_entry_per_hour(
        start_date,
        end_date,
        id_campaign,
        id_agent
    )

    call_entry_count = count_calls.count_call_entry(start_date, end_date, id_agent, id_campaign)

    longest_wait_queue_call = queue_stadistics.get_longest_wait_queue_call(
        id_campaign
    )

    average_queue_wait = queue_stadistics.get_average_wait(
        start_date, end_date, id_agent, id_campaign
    )

    answered_befrore, seconds = tmo_calls.get_answered_before(
        start_date, end_date, id_agent, id_campaign
    )

    call_entry_count['before'] = answered_befrore

    service_level = tmo_calls.get_service_level(answered_befrore, call_entry_count['total'])
    tmo = tmo_calls.get_tmo(answered_befrore, call_entry_count['terminada'])
    effectiveness = tmo_calls.get_effectiveness(
        call_entry_count['terminada'], call_entry_count['total']
    )

    agents_logged, agent_list = agent_state_count.get_agents_logged()
    agents_in_break = agent_state_count.get_agents_in_break(agent_list)
    agents_in_call = agent_state_count.get_agents_in_call()

    response = {
        'call_entry_per_hour': call_entry_per_hour,
        'call_entry_count': call_entry_count,
        'longest_wait_queue_call': longest_wait_queue_call,
        'average_queue_wait': average_queue_wait,
        'service_level': service_level,
        'tmo': tmo,
        'effectiveness': effectiveness,
        'seconds': seconds,
        'agents_logged': agents_logged,
        'agents_in_break': agents_in_break,
        'agents_in_call': agents_in_call
    }

    return response

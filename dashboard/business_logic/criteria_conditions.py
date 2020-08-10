"""Manage common functions shared by the dashboard logic"""
from datetime import timedelta, datetime

def get_call_criteria(start_date, end_date, agent, campaign):
    """Returns a conditions dictonary"""
    conditions = {}
    if (start_date != "" and end_date != ""):
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        conditions['datetime_entry_queue__range'] = (start_date, end_date)
    elif start_date != "":
        conditions['datetime_entry_queue__gte'] = start_date
    elif end_date != "":
        conditions['datetime_entry_queue__lte'] = start_date

    if agent != "":
        conditions['agent'] = agent

    if campaign != "":
        conditions['id_campaign'] = campaign

    return conditions
"""Manages functions for calculating outgoing calls graphic stats values"""
from datetime import datetime, timedelta
import pytz
from agent_console.models import Calls
from consolidacion.models import CallConsolidacion, Consolidacion

def get_today_pending_consolidacion(start_date, end_date):
    """Gets the number of pending calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_filter(start_date, end_date)
    ).values_list('call', flat=True))
    pending_consolidacion = Calls.objects.filter(id__in=today_consolidations, status__isnull=True)
    return pending_consolidacion.count()

def get_today_consolidacion(start_date, end_date):
    """Gets the number of calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_filter(start_date, end_date)
    ).values_list('call', flat=True))
    today_consolidacion = Calls.objects.filter(id__in=today_consolidations)
    return today_consolidacion.count()

def get_success_consolidacion(start_date, end_date):
    """Gets the number of success calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_filter(start_date, end_date, True)
    ).values_list('call', flat=True))
    success_consolidacion = Calls.objects.filter(id__in=today_consolidations, status='Success')
    return success_consolidacion.count()

def get_scheduled_consolidacion(start_date, end_date):
    """Gets the number of success calls for the current date"""
    criteria = get_filter(start_date, end_date, True)
    criteria['cita_tall_id__isnull'] = False
    today_scheduled = CallConsolidacion.objects.filter(
        **criteria
    )
    return today_scheduled.count()

def get_dialed_consolidacion(start_date, end_date):
    """Gets the number of dialed calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_filter(start_date, end_date, True)
    ).values_list('call', flat=True))
    dialed_consolidacion = Calls.objects.filter(id__in=today_consolidations, status__isnull=False)
    return dialed_consolidacion.count()

def get_filter(start_date, end_date, made=False):
    """Gets filter condition for query today consolidations"""
    conditions = {}
    if (start_date != "" and end_date != ""):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        conditions['consolidacion__fecha__range'] = (start_date, end_date)
    elif start_date != "":
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        conditions['consolidacion__fecha__gte'] = start_date
    elif end_date != "":
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(seconds=86399)
        conditions['consolidacion__fecha__lte'] = end_date
    conditions['call_made'] = made
    return conditions

def get_completion_rate(pending, total):
    """Computes effectiveness level"""
    done = total - pending
    if total > 0:
        completion = done/total * 100
    else:
        completion = 100
    return "%.2f" % completion

def get_success_rate(success, dialed):
    """Computes effectiveness level"""
    if dialed > 0:
        completion = success/dialed * 100
    else:
        completion = 100
    return "%.2f" % completion


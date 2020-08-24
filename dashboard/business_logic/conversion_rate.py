"""Manages functions for calculating outgoing calls graphic stats values"""
from datetime import datetime, timedelta
import pytz
from agent_console.models import Calls
from consolidacion.models import CallConsolidacion

def get_today_pending_consolidacion():
    """Gets the number of pending calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_today_filter()
    ).values_list('call', flat=True))
    pending_consolidacion = Calls.objects.filter(id__in=today_consolidations, status__isnull=True)
    return pending_consolidacion.count()

def get_today_consolidacion():
    """Gets the number of calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_today_filter()
    ).values_list('call', flat=True))
    today_consolidacion = Calls.objects.filter(id__in=today_consolidations)
    return today_consolidacion.count()

def get_success_consolidacion():
    """Gets the number of success calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_today_filter(True)
    ).values_list('call', flat=True))
    success_consolidacion = Calls.objects.filter(id__in=today_consolidations, status='Success')
    return success_consolidacion.count()

def get_dialed_consolidacion():
    """Gets the number of dialed calls for the current date"""
    today_consolidations = list(CallConsolidacion.objects.filter(
        **get_today_filter(True)
    ).values_list('call', flat=True))
    dialed_consolidacion = Calls.objects.filter(id__in=today_consolidations, status__isnull=False)
    return dialed_consolidacion.count()

def get_today_filter(made=False):
    """Gets filter condition for query today consolidations"""
    timezone = pytz.timezone("America/Bogota")
    today_aware = timezone.localize(datetime.today())
    today_filter = {
        'consolidacion__fecha__lte': today_aware + timedelta(seconds=86399),
        'call_made': made
    }
    return today_filter

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


"""Includes the data filters for pickers and datatables in the sedes app"""
from django.db.models import Q
from agent_console.models import Campaign

def campaign_picker_filter(value):
    """Given a value, filters sedes for a select picker"""
    return list(Campaign.objects.filter(
        Q(name__contains=value)
    )[:10])

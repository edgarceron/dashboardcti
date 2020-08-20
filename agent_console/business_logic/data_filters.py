"""Includes the data filters for pickers and datatables in the sedes app"""
from django.db.models import Q
from agent_console.models import Campaign, Agent

def campaign_picker_filter(value):
    """Given a value, filters campaign for a select picker"""
    return list(Campaign.objects.filter(
        Q(name__icontains=value)
    )[:10])

def agent_picker_filter(value):
    """Given a value, filters agent for a select picker"""
    return list(Agent.objects.filter(
        Q(name__icontains=value) |
        Q(number__icontains=value)
    )[:10])

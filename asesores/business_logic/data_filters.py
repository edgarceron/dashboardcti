"""Includes the data filters for pickers and datatables in the asesores app"""
from django.db.models import Q
from asesores.models import Asesor

def asesor_picker_filter(value):
    """Given a value, filters asesores for a select picker"""
    return list(Asesor.objects.filter(
        Q(active=True),
        Q(name__icontains=value)
    )[:10])

def asesor_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Asesor.objects.filter(
            Q(name__icontains=search)
        ).count()

    return Asesor.objects.filter(
        Q(name__icontains=search)
    )[start:start + length]

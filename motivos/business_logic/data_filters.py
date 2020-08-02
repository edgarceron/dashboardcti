"""Includes the data filters for pickers and datatables in the motivos app"""
from django.db.models import Q
from motivos.models import Motivo

def motivo_picker_filter(value):
    """Given a value, filters motivos for a select picker"""
    return list(Motivo.objects.filter(
        Q(active=True),
        Q(name__icontains=value)
    )[:10])

def motivo_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Motivo.objects.filter(
            Q(name__icontains=search)
        ).count()

    return Motivo.objects.filter(
        Q(name__icontains=search)
    )[start:start + length]

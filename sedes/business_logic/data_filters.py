"""Includes the data filters for pickers and datatables in the sedes app"""
from django.db.models import Q
from dms.models import Bodegas
from sedes.models import Sede

def sede_picker_filter(value):
    """Given a value, filters sedes for a select picker"""
    return list(Sede.objects.filter(
        Q(active=True),
        Q(name__icontains=value)
    )[:10])

def bodegas_picker_filter(value):
    """Given a value, filters sedes for a select picker"""
    return list(Bodegas.objects.filter(
        Q(descripcion__icontains=value) | Q(bodega__icontains=value)
    )[:10])

def sede_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Sede.objects.filter(
            Q(name__icontains=search)
        ).count()

    return Sede.objects.filter(
        Q(name__icontains=search)
    )[start:start + length]

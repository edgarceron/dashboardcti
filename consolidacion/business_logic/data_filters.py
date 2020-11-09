"""Includes the data filters for pickers and datatables in the sedes app"""
from django.db.models import Q
from consolidacion.models import Consolidacion

def consolidacion_picker_filter(value):
    """Given a value, filters sedes for a select picker"""
    return list(Consolidacion.objects.filter(
        Q(active=True),
        Q(placa__icontains=value) | Q(cedula__icontains=value)
    )[:10])

def consolidacion_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Consolidacion.objects.filter(
            Q(placa__icontains=search) | Q(cedula__icontains=search) | Q(fecha__icontains=search)
        ).count()

    return Consolidacion.objects.filter(
        Q(placa__icontains=search) | Q(cedula__icontains=search) | Q(fecha__icontains=search)
    )[start:start + length]



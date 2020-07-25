"""Includes the data filters for pickers and datatables in the sedes app"""
from django.db.models import Q
from sedes.models import Sede

def consolidacion_picker_filter(value):
    """Given a value, filters sedes for a select picker"""
    return list(Sede.objects.filter(
        Q(active=True),
        Q(placa__contains=value) | Q(cedula__contaions=value)
    )[:10])

def consolidacion_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Sede.objects.filter(
            Q(placa__contains=search) | Q(cedula__contaions=search)
        ).count()

    return Sede.objects.filter(
        Q(placa__contains=search) | Q(cedula__contaions=search)
    )[start:start + length]

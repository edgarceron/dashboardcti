"""Includes the data filters for pickers and datatables in the form_creator app"""
from django.db.models import Q
from form_creator.models import Form

def form_picker_filter(value):
    """Given a value, filters forms for a select picker"""
    return list(Form.objects.filter(
        Q(active=True),
        Q(name__contains=value)
    )[:10])

def form_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Form.objects.filter(
            Q(name__contains=search)
        ).count()

    return Form.objects.filter(
        Q(name__contains=search)
    )[start:start + length]

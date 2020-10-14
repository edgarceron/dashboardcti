"""Includes the data filters for pickers and datatables in the campaigns app"""
from django.db.models import Q
from campaings.models import CampaignForm

def campaign_picker_filter(value):
    """Given a value, filters campaigns for a select picker"""
    return list(CampaignForm.objects.filter(
        Q(name__icontains=value)
    )[:10])

def campaign_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return CampaignForm.objects.filter(
            Q(name__icontains=search)
        ).count()

    return CampaignForm.objects.filter(
        Q(name__icontains=search)
    )[start:start + length]

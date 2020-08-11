"""Includes the data filters for pickers and datatables in the profiles app"""
from django.db.models import Q
from profiles.models import Profile

def profile_picker_filter(value):
    """Given a value, filters profiles for a select picker"""
    return list(Profile.objects.filter(
        Q(active=True),
        Q(name__icontains=value)
    )[:10])


def profiles_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return Profile.objects.filter(
            Q(name__icontains=search)
        ).count()

    return Profile.objects.filter(
        Q(name__icontains=search)
    )[start:start + length]

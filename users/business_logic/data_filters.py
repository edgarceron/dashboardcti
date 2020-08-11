"""Includes the data filter for pickers and datatables in the users app"""
from django.db.models import Q
from users.models import User

def users_picker_filter(value):
    """Looks for users wich contain the given value in their data"""
    return list(User.objects.filter(
        Q(active=True),
        Q(username__icontains=value) | Q(name__icontains=value) | Q(lastname__icontains=value)
    )[:10])

def users_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return User.objects.filter(
            Q(username__icontains=search) | Q(name__icontains=search)
            | Q(lastname__icontains=search)
        ).count()

    return User.objects.filter(
        Q(username__icontains=search) | Q(name__icontains=search)
        | Q(lastname__icontains=search)
    )[start:start + length]

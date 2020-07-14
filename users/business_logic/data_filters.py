"""Includes the data filter for pickers and datatables in the users app"""
from django.db.models import Q
from users.models import User

def users_picker_filter(value):
    """Looks for users wich contain the given value in their data"""
    return list(User.objects.filter(
        Q(active=True),
        Q(username__contains=value) | Q(name__contains=value) | Q(lastname__contains=value)
    )[:10])

def users_listing_filter(search, start, length, count=False):
    """Filters the corresponding models given a search string"""
    if count:
        return User.objects.filter(
            Q(username__contains=search) | Q(name__contains=search)
            | Q(lastname__contains=search)
        ).count()

    return User.objects.filter(
        Q(username__contains=search) | Q(name__contains=search)
        | Q(lastname__contains=search)
    )[start:start + length]

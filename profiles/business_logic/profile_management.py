"""Manges the profile crud genereal functions"""
import json
from profiles.serializers import ProfilePermissionsSerializer
from profiles.models import ProfilePermissions

def manage_profile_actions(request, profile_serializer):
    """Creates or updates the actión for a given profile"""
    json_actions = request.data['actions']
    actions = json.loads(json_actions)
    profile_id = profile_serializer.data['id']
    for element in range(0, len(actions)):
        action_id = actions[element]['action']
        try:
            permission_obj = ProfilePermissions.objects.get(
                profile=profile_id, action=action_id)
            actions[element]['profile'] = profile_id
            permission_serializer = ProfilePermissionsSerializer(
                permission_obj, data=actions[element])
        except ProfilePermissions.DoesNotExist:
            actions[element]['profile'] = profile_id
            permission_serializer = ProfilePermissionsSerializer(data=actions[element])

        if permission_serializer.is_valid():
            permission_serializer.save()

def concat_profile_actions(request, data):
    """Adds the profile actions to the data"""
    profile_id = data["data"]["id"]
    permission_list = ProfilePermissions.objects.filter(profile=profile_id)
    permissions_serializer = ProfilePermissionsSerializer(permission_list, many=True)
    data["actions"] = permissions_serializer.data
    return data

from rest_framework.response import Response
from rest_framework import status
from users.permission_validation import PermissionValidation

def check_current_user(request, user_id):
    """Verifies that the profile that's going to be deleted
    is not the same as the current user profile"""
    current_user = PermissionValidation(request).user
    if current_user.id == user_id:
        return False
    return True

def current_user_cannot_be_deleted_message():
    data = {
        "success": False,
        "message":"No puede eliminar su propio usuario."
    }
    return Response(data, status=status.HTTP_409_CONFLICT, content_type='application/json')

from django.shortcuts import render
from users.permission_validation import PermissionValidation

# Create your views here.
def get_actions():
    actions = [
       {"name": "dashboard", "label": "Pagina principal del modulo de dashboard"},
    ]
    return actions

def dashboard(request, user_id=0):
    "Returns the rendered for the dashboard."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_motivo')
    if validation['status']:
        return render(
            request,
            'dashboard/dashboard.html',
            {
                'id':user_id,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

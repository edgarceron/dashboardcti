"""Handles the views for the dasbboard app"""
from django.shortcuts import render
from users.permission_validation import PermissionValidation

# Create your views here.
def get_actions():
    """Returns the actions for this views file"""
    actions = [
        {"name": "dashboard", "label": "Pagina principal del modulo de dashboard"},
        {"name": "dashboard_options_form", "label": "Pagina de las opciones del dashboard"},
    ]
    return actions

def dashboard(request, user_id=0):
    "Returns the rendered for the dashboard."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('dashboard')
    if validation['status']:
        return render(
            request,
            'dashboard/dashboard.html',
            #'maingui/under_construction.html',
            {
                'id':user_id,
                'username': permission_obj.user.name
            }
        )
    return permission_obj.error_response_view(validation, request)

def dashboard_options_form(request):
    "Returns the rendered template for the given user."
    
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('dashboard_options_form')
    if validation['status']:
        data = {
            'username': permission_obj.user.name
        }

        return render(
            request,
            'dashboard/options_form.html',
            data
        )
    return permission_obj.error_response_view(validation, request)

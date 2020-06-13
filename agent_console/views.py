""" Contains the view for the agent consoole module"""
from django.shortcuts import render
from users.permission_validation import PermissionValidation
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "form_user_agent", "label": "Webservice enlazar usuario con agente de call center"},
    ]
    return actions

def form_user_agent(request, user_id=0):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_user_agent')
    if validation['status']:
        if user_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'agent_console/form.html',
            {
                'id':user_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)
# Create your views here.

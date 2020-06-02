"Contains the views for the users app."
from django.shortcuts import render

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "form_user", "label": "Pagina del formulario de usuario"},
        {"name": "listing_user", "label": "Pagina del listado de usuarios"}
    ]
    return actions

def form(request, user_id=0):
    "Returns the rendered template for the given user."
    if user_id == 0:
        action = "Crear"
    else:
        action = "Actualizar"
    #TODO verificar usuario y permisos

    return render(
        request,
        'users/form.html',
        {
            'id':user_id,
            'action':action,
            'username': "Mauricio"
        }
    )

def listing(request):
    "Returns the rendered template for user listing."
    #TODO verificar usuario y permisos
    return render(
        request,
        'users/listing.html',
        {
            'username': "Mauricio"
        }
    )

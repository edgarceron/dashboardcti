from django.shortcuts import render

# Create your views here.
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "listing", "label": "Pagina de listado del modulo de perfiles"},
        {"name": "form", "label": "Pagina de formulario del modulo de perfiles"}
    ]
    return actions

def form(request, profile_id=0):
    "Returns the rendered template for the given profile."
    if profile_id == 0:
        action = "Crear"
    else:
        action = "Actualizar"
    #TODO verificar usuario y permisos

    return render(
        request,
        'profiles/form.html',
        {
            'id':profile_id,
            'action':action,
            'username': "Mauricio"
        }
    )

def listing(request):
    "Returns the rendered template for profile listing."
    #TODO verificar usuario y permisos
    return render(
        request,
        'profiles/listing.html',
        {
            'username': "Mauricio"
        }
    )

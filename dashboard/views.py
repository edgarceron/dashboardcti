from django.shortcuts import render

# Create your views here.
def get_actions():
    actions = [
       #{"name": "index", "label": "Pagina principal del modulo de dashboard"},
    ]
    return actions

def dashboard(request, user_id=0):
    "Returns the rendered template for the given user."

    return render(
        request,
        'dashboard/dashboard.html',
        {
            'id':user_id,
            'username': "Mauricio"
        }
    )
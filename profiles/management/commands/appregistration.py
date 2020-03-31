from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from profiles.models import Action, App
from profiles.serializers import ActionSerializer, AppSerializer
import importlib

class Command(BaseCommand):

    def handle(self, *args, **options):
        for app in settings.WEB_APPS:
            app_serializer = AppSerializer(data = {"name":app})
            if(app_serializer.is_valid()):
                app_serializer.save()
                self.stdout.write("Se creo la App " + app)
            else:
                self.stdout.write("Ya existe la app " + app)
            
        registered_apps = App.objects.all()


        for app in registered_apps:
            setted = False
            
            for setted_app in settings.WEB_APPS:
                if(app.name == setted_app):
                    setted = True

            if(setted):
                app_id      = app.id
                name        = app.name
                views       = importlib.import_module(name + ".views")
                webservices = importlib.import_module(name + ".webservices")

                actions = views.get_actions() + webservices.get_actions()

                for action in actions:
                    data = {"name": action["name"], "label": action["label"], "app": app_id}
                    action_serializer = ActionSerializer(data = data)
                    if(action_serializer.is_valid()):
                        try:
                            action_serializer.save()
                            self.stdout.write("Se creo la acción " + action["name"] + " para el modulo " + name)
                        except:
                            self.stdout.write("Ya existe la acción " + action["name"] + " para el modulo " + name)
            else:
                app.delete()      

        

        
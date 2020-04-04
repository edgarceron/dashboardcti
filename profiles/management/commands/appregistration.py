from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from profiles.models import Action, App
from profiles.serializers import ActionSerializer, AppSerializer
import importlib

class Command(BaseCommand):

    def create_apps(self):
        for app in settings.WEB_APPS:
            app_serializer = AppSerializer(data = {"name":app})
            if(app_serializer.is_valid()):
                app_serializer.save()
                self.stdout.write("Se creo la App " + app)
            else:
                self.stdout.write("Ya existe la app " + app)

    def delete_removed_apps(self, registered_apps):
        for app in registered_apps:
            setted = False
            
            for setted_app in settings.WEB_APPS:
                if(app.name == setted_app):
                    setted = True

            if(not setted):
                self.stdout.write("Se elimino la app " + app.name + " y todas sus acciones")
                app.delete()

    @staticmethod
    def get_actions(app_name, file_name):
        try:
            file = importlib.import_module(app_name + "." + file_name)
            actions = file.get_actions()
        except:
            actions = []
        
        return actions
    
    def delete_removed_actions(self, registered_actions, app_id, app_name):
        setted_actions = Action.objects.filter(app = app_id)

        for action in setted_actions:
            setted = False
            
            for registered_action in registered_actions:
                if(registered_action["name"] == action.name):
                    setted = True
                    break

            if(not setted):
                self.stdout.write("Se elimino la acción " + action.name + " de la app " + app_name)
                action.delete()
                
    def create_actions(self, registered_actions, app_id, app_name):
        for action in registered_actions:
            data = {"name": action["name"], "label": action["label"], "app": app_id}
            action_serializer = ActionSerializer(data = data)
            if(action_serializer.is_valid()):
                try:
                    action_serializer.save()
                    self.stdout.write("Se creo la acción " + action["name"] + " para el modulo " + app_name)
                except:
                    self.stdout.write("Ya existe la acción " + action["name"] + " para el modulo " + app_name)

    def handle(self, *args, **options):
        registered_apps = App.objects.all()
        self.delete_removed_apps(registered_apps)
        self.create_apps()
        
        for app in registered_apps:
            app_id             = app.id
            app_name           = app.name
            views              = Command.get_actions(app_name, 'views')
            webservices        = Command.get_actions(app_name, 'webservices')
            registered_actions = views + webservices

            self.delete_removed_actions(registered_actions, app_id, app_name)
            self.create_actions(registered_actions, app_id, app_name)

            

        

        
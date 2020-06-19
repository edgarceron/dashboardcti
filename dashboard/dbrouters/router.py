class IntegrationRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    call_center_tables = {
        'agent',
        'audit',
        'break',
        'callattribute',
        'callentry',
        'callprogresslog',
        'callrecording',
        'calls',
        'campaign',
        'campaignentry',
        'campaignexternalurl',
        'campaignform',
        'campaignformentry',
        'contact',
        'currentcallentry',
        'currentcalls',
        'dontcall',
        'eccpauthorizedclients',
        'form',
        'formdatarecolected',
        'formdatarecolectedentry',
        'formfield',
        'queuecallentry',
        'valorconfig',
        'cedulallamada'
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read call_center models go to call_center.
        """
        if model._meta.db_table in self.call_center_tables:
            return 'call_center'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write call_center models go to call_center.
        """
        if model._meta.db_table in self.call_center_tables:
            return 'call_center'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the default or call_center table is
        involved.
        """
        if (
                obj1._meta.db_table in self.call_center_tables or
                obj2._meta.db_table in self.call_center_tables
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the call_center tables only appear in the
        'call_center' database.
        """
        if model_name in self.call_center_tables:
            if db == 'call_center':
                print(model_name)
                return True
        return None

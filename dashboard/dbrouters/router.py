class IntegrationRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    call_center_models = {
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

    call_center_tables = {
        'agent',
        'audit',
        'break',
        'call_attribute',
        'call_entry',
        'call_progress_log',
        'call_recording',
        'calls',
        'campaign',
        'campaign_entry',
        'campaign_external_url',
        'campaign_form',
        'campaign_form_entry',
        'contact',
        'current_call_entry',
        'current_calls',
        'dont_call',
        'eccp_authorized_clients',
        'form',
        'form_data_recolected',
        'form_data_recolected_entry',
        'form_field',
        'queue_call_entry',
        'valor_config',
        'cedula_llamada'
    }

    dms_models = {
        'tallconceptosoperaciones',
        'tercerosactividadeconomica',
        'condicionespago',
        'referencias',
        'tallcitas',
        'sedesdebodegas',
        'terceros',
        'bodegas',
        'wtallcitasbahias',
        'wtallcitascausascancelacion',
        'referenciasgen',
        'referenciascla',
        'referenciascla',
        'referenciascon',
        'referenciassub3',
        'terceros1',
        'terceros2',
        'terceros3',
        'terceros4',
        'terceros5',
        'terceros6',
        'terceros7',
        'terceros8',
        'terceros9',
        'terceros10',
        'tercerosica',
        'tercerosactividadescree',
        'wtallcitastipobahia',
        'centros',
        'centrosgrupos',
        'centrossubgrupos',
        'wtallcitastipotecnico',
        'tallcitasauditoria',
        'crmcitas',
        'tallcitasoperaciones',
        'talltempario',
        'referenciasimp'
    }

    dms_tables = {
        'tall_conceptos_operaciones',
        'Terceros_actividad_economica',
        'condiciones_pago',
        'referencias',
        'tall_citas',
        'SedesDeBodegas',
        'terceros',
        'bodegas',
        'w_tall_citas_bahias',
        'w_tall_citas_Causas_Cancelacion',
        'referencias_gen',
        'referencias_cla',
        'referencias_con',
        'referencias_sub3',
        'terceros_1',
        'terceros_2',
        'terceros_3',
        'terceros_4',
        'terceros_5',
        'terceros_6',
        'terceros_7',
        'terceros_8',
        'terceros_9',
        'terceros_10',
        'terceros_ica',
        'terceros_actividades_cree',
        'w_tall_citas_tipoBahia',
        'centros',
        'centros_grupos',
        'centros_subgrupos',
        'w_tall_citas_tipoTecnico',
        'tall_citas_auditoria',
        'CRM_citas',
        'tall_citas_operaciones',
        'tall_tempario',
        'referencias_imp'
    }

    def db_for_read(self, model, **hints):
        """
        Attempts to read call_center models go to call_center.
        """
        if model._meta.db_table in self.call_center_tables:
            return 'call_center'
        if model._meta.db_table in self.dms_tables:
            return 'caribe_dms'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write call_center models go to call_center.
        """
        if model._meta.db_table in self.call_center_tables:
            return 'call_center'
        if model._meta.db_table in self.dms_tables:
            return 'caribe_dms'
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
        if model_name in self.call_center_models:
            if db == 'call_center':
                return True
        if model_name in self.dms_models:
            if db == 'caribe_dms':
                return True
        return None

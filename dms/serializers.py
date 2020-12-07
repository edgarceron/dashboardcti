"""Contains the serializers for the dms module"""
from rest_framework import serializers
from consolidacion.models import CallConsolidacion, CallEntryCita, CitaNoCall
from .models import CrmCitas, TallCitas, Terceros

def get_observaciones(id_cita):
    try:
        observaciones = CallConsolidacion.objects.get(cita_tall_id=id_cita).observaciones
    except CallConsolidacion.DoesNotExist:
        try:
            observaciones = CallEntryCita.objects.get(cita_tall_id=id_cita).observaciones
        except CallEntryCita.DoesNotExist:
            try:
                observaciones = CitaNoCall.objects.get(cita_tall_id=id_cita).observaciones
            except CitaNoCall.DoesNotExist:
                observaciones = ""
    observaciones.replace('\r\n', " ").replace('\n', " ").replace('\t', " ")
    return observaciones

class CrmCitasSerializer(serializers.ModelSerializer):
    """Serializer for CrmCitas model"""
    class Meta:
        model = CrmCitas
        fields = '__all__'

    def create(self, validated_data):
        obj = CrmCitas(**validated_data)
        obj.save()
        return obj

class TallCitasSerializer(serializers.ModelSerializer):
    """Serializer for TallCitas model"""
    class Meta:
        model = TallCitas
        fields = [
            'bodega',
            'fecha_hora_creacion',
            'estado_cita',
            #'descripcion_estado',
            'fecha_hora_ini',
            'fecha_hora_fin',
            'hora',
            'minutos',
            'duracion_minutos',
            'codigo_veh',
            'placa',
            'nit',
            'nombre_cliente',
            'nit_nuevo',
            'nombre_encargado',
            'telefonos',
            'notas',
            'ano_veh',
            'usuario',
            'pc',
            'modulo',
            'mail',
            'asesor',
            'numerocomfrimaciones',
            'numeroespacios',
            'facturado',
        ]

    def to_representation(self, instance):
        representation = super(TallCitasSerializer, self).to_representation(instance)
        representation['fecha_hora_ini'] = instance.fecha_hora_ini.strftime("%I:%M:%S %p")
        return representation

    def create(self, validated_data):
        obj = TallCitas(**validated_data)
        obj.save()
        return obj

class TallCitasSerializerSimple(serializers.ModelSerializer):
    """Serializer for TallCitas model"""
    class Meta:
        model = TallCitas
        fields = [
            'id_cita',
            'bodega',
            'fecha_hora_ini',
            'placa',
            'nit',
            'nombre_cliente',
            'nombre_encargado',
            'telefonos',
            'notas',
            'mail',
            'asesor',
            'estado_cita'
        ]

    def to_representation(self, instance):
        representation = super(TallCitasSerializerSimple, self).to_representation(instance)
        representation['fecha_hora_ini'] = instance.fecha_hora_ini.strftime("%Y-%m-%d %I:%M:%S %p")
        representation['notas'] = get_observaciones(representation['id_cita'])
        return representation

class TercerosSerializer(serializers.ModelSerializer):
    """Serializer for Terceros model"""
    class Meta:
        model = Terceros
        fields = ['nit', 'nombres', 'mail']

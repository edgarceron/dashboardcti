"""Contains the serializers for the dms module"""
from rest_framework import serializers
from .models import CrmCitas, TallCitas

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

    def create(self, validated_data):
        obj = TallCitas(**validated_data)
        obj.save()
        return obj

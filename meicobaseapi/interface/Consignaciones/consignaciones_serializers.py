import uuid
from rest_framework import serializers
from meicobaseapi.models import Consignaciones

class ConsignacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignaciones
        fields = '__all__'
        extra_kwargs = {
            'tipo_consignacion': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': 'El tipo de consignación es requerido.',
                    'blank': 'El tipo de consignación no puede estar vacío.',
                    'null': 'El tipo de consignación es requerido.',
                }
            },
            'numero_guia': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': 'El número de guía es requerido.',
                    'blank': 'El número de guía no puede estar vacío.',
                    'null': 'El número de guía es requerido.',
                }
            },
            'ruta_archivo_soporte': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': 'La ruta del archivo de soporte es requerida.',
                    'blank': 'La ruta del archivo no puede estar vacía.',
                    'null': 'La ruta del archivo de soporte es requerido.',
                }
            },
            'valor_consignacion': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': 'El valor de la consignación es requerido.',
                    'invalid': 'El valor debe ser un número decimal válido.',
                    'null': 'El valor es requerido.',
                }
            },
            'numero_planilla': {
                'required': True,
                'error_messages': {
                    'required': 'El número de planilla es requerido.',
                    'blank': 'El número de planilla no puede estar vacío.',
                    'null': 'El número de planilla es requerido',
                }
            },
        }

        
        
class ConsignacionesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignaciones
        fields = '__all__'
       
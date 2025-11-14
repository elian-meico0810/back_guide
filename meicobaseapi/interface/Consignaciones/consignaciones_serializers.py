import uuid
from rest_framework import serializers
from meicobaseapi.models import Consignaciones

class ConsignacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignaciones
        fields = '__all__'
        extra_kwargs = {
            'TipoConsignacion': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': 'El tipo de consignación es requerido.',
                    'blank': 'El tipo de consignación es requerido',
                    'null': 'El tipo de consignación es requerido.',
                }
            },
            'NumeroGuia': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': 'El número de guía es requerido.',
                    'blank': 'El número de guía es requerido.',
                    'null': 'El número de guía es requerido.',
                }
            },
            'RutaArchivoSoporte': {
                'required': True,
                'allow_blank': False,
                'allow_null': False,
                'error_messages': {
                    'required': 'La ruta del archivo de soporte es requerida.',
                    'blank': 'La ruta del archivo es requerido',
                    'null': 'La ruta del archivo de soporte es requerido.',
                }
            },
            'ValorConsignacion': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': 'El valor de la consignación es requerido.',
                    'invalid': 'El valor debe ser un número decimal válido.',
                    'null': 'El valor de la consignación es requerido.',
                }
            },
            'NumeroPlanilla': {
                'required': True,
                'error_messages': {
                    'required': 'El número de planilla es requerido.',
                    'blank': 'El número de planilla es requerido',
                    'null': 'El número de planilla es requerido',
                }
            },
            'NombreArchivo': {
                'required': True,
                'allow_null': False,
                'error_messages': {
                    'required': 'El nombre del archivo es requerido.',
                    'invalid': 'El nombre del archivo es requerido',
                    'null': 'El nombre del archivo es requerido.',
                }
            },
        }
        

    def validate(self, data):
        try:
            valor_consignacion = data.get('ValorConsignacion',0)
            if not valor_consignacion or valor_consignacion <= 0:
                raise Exception("El valor de la consignación de ser mayor a 0.")
            return data
        except Exception as e:
            raise e
        
        
class ConsignacionesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignaciones
        fields = '__all__'
       
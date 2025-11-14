from rest_framework import serializers
from meicobaseapi.models import PlanillaDetalles


class PlanillaDetallesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanillaDetalles
        fields = '__all__'


class PlanillaDetallesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanillaDetalles
        fields = '__all__'
       
       
class PlanillaWsSerializer(serializers.Serializer):
    bodega_id = serializers.CharField(
        required=True,
        error_messages={
            'required': 'El campo bodega_id es obligatorio.',
            'invalid': 'El id de la bodega no es válido.'
        },
        validators=[]
    )
    fecha = serializers.RegexField(
        regex=r'^\d{4}-\d{2}-\d{2}$',
        required=True,
        error_messages={
            'required': 'El campo fecha es obligatorio.',
            'invalid': 'El formato de la fecha debe ser YYYY-MM-DD (año-mes-día).'
        },
        validators=[]
    )    
from rest_framework import serializers
from meicobaseapi.models import PlanillaEncabezado

class PlanillaEncabezadoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanillaEncabezado
        fields = '__all__'
       
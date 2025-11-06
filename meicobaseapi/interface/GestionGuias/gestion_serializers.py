from rest_framework import serializers
from meicobaseapi.models import PlanillaDetalles, PlanillaEncabezado

class PlanillaDetallesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanillaDetalles
        fields = '__all__'
        
        
class PlanillaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanillaEncabezado
        fields = '__all__'
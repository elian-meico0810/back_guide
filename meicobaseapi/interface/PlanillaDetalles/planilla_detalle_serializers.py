import uuid
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
       
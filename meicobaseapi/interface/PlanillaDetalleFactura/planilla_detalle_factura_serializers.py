import uuid
from rest_framework import serializers
from meicobaseapi.models import PlanillaDetalleFactura

class PlanillaDetalleFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanillaDetalleFactura
        fields = '__all__'

class PlanillaDetalleFacturaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanillaDetalleFactura
        fields = '__all__'
       
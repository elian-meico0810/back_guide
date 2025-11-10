from rest_framework import serializers
from meicobaseapi.models import Consignaciones


class ConsignacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignaciones
        fields = '__all__'
        
        
class ConsignacionesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consignaciones
        fields = '__all__'
       
from rest_framework import serializers
from meicobaseapi.models import Roles

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
        extra_kwargs = {
            'nombre': {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "error_messages": {
                    "invalid": "El nombre no es válido.",
                    "required": "El nombre es requerido.",
                    "blank": "El nombre no puede estar vacío.",
                    "null": "El nombre no puede ser nulo.",
                }
            },
        }
        

class RolesUpdatedSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Roles
        fields = ['nombre', 'descripcion', 'estado']
        extra_kwargs = {
            'nombre': {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "error_messages": {
                    "invalid": "El nombre no es válido.",
                    "required": "El nombre es requerido.",
                    "blank": "El nombre no puede estar vacío.",
                    "null": "El nombre no puede ser nulo.",
                }
            },
        }
        

class UsuariosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = ['nombre', 'descripcion', 'estado']
        
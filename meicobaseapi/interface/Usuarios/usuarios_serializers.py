from rest_framework import serializers
from meicobaseapi.models import Usuarios
from meicobaseapi.core.APIResponse import APIResponse

class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
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
            'correo': {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "error_messages": {
                    "invalid": "El correo no es válido.",
                    "required": "El correo es requerido.",
                    "blank": "El correo no puede estar vacío.",
                    "null": "El correo no puede ser nulo.",
                }
            },
        }
        


class UsersariosUpdatedSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Usuarios
        fields = ['nombre', 'correo', 'ciudad', 'estado']
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
            'correo': {
                "required": True,
                "allow_null": False,
                "allow_blank": False,
                "error_messages": {
                    "invalid": "El correo no es válido.",
                    "required": "El correo es requerido.",
                    "blank": "El correo no puede estar vacío.",
                    "null": "El correo no puede ser nulo.",
                }
            },
        }
        

class UsuariosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['id', 'nombre', 'correo', 'ciudad', 'estado']
        
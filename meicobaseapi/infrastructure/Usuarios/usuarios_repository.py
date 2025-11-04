from meicobaseapi.models import Usuarios
from django.db import connection
from django.db import transaction
from django.utils import timezone

class UsuariosRepository:
    
    
    def get_all(self):
        try:
            data = Usuarios.objects.filter(estado=True)
            if not data: raise Exception("Usuario no encontrado")
            return data
        except Exception as e:
            raise e
    
    
    def get_by_email(self, email):
        try:
            data = Usuarios.objects.filter(correo=email, estado=True).first()
            if not data: raise Exception("Usuario no encontrado")
            return data
        except Exception as e:
            raise e
        
    
    def create(self, data):
        try:
            return Usuarios.objects.create(**data)
        except Exception as e:
            raise e
        
    
    def update(self, id, auth_user, data):
        try:
            with transaction.atomic():
                usuario = Usuarios.objects.get(id=id)
                usuario.nombre = data.get("nombre", usuario.nombre)
                usuario.correo = data.get("correo", usuario.correo)
                usuario.ciudad = data.get("ciudad", usuario.ciudad)
                usuario.updated_by = auth_user
                usuario.updated_at = timezone.now()
                usuario.save()
            return usuario
        except Exception as e:
            raise e


    def delete(self, user_id, auth_user=None):
        try:
            with transaction.atomic():

                usuario = Usuarios.objects.get(id=user_id)
                usuario.estado = False
                usuario.deleted_by = auth_user
                usuario.deleted_at = timezone.now()
                usuario.save()
            return True
        except Exception as e:
            raise e

    

    def get_by_id(self, user_id):
        try:
            data = Usuarios.objects.filter(id=user_id, estado=True).first()
            if not data: raise Exception("Usuario no encontrado")
            return data
        except Exception as e:
            raise e


from meicobaseapi.models import Roles
from django.db import connection
from django.db import transaction
from django.utils import timezone

class RolesRepository:
    
    
    def get_all(self):
        try:
            data = Roles.objects.filter(estado=True).first()
            if not data: raise Exception("Rol no encontrado")
            return data
        except Exception as e:
            raise e
    
    
    def get_by_name(self, name):
        try:
            data =  Roles.objects.filter(nombre=name, estado=True).first()
            if not data: raise Exception("Rol no encontrado")
            return data
        except Exception as e:
            raise e
        
    
    def create(self, data):
        try:
            return Roles.objects.create(**data)
        except Exception as e:
            raise e
        
    
    def update(self, id, auth_user, data):
        try:
            with transaction.atomic():
                rol = Roles.objects.get(id=id)
                rol.nombre = data.get("nombre", rol.nombre)
                rol.descripcion = data.get("descripcion", rol.descripcion)
                rol.updated_at = timezone.now()
                rol.save()
            return rol
        except Exception as e:
            raise e


    def delete(self, user_id, auth_user=None):
        try:
            with transaction.atomic():

                rol = Roles.objects.get(id=user_id)
                rol.estado = False
                rol.deleted_by = auth_user
                rol.deleted_at = timezone.now()
                rol.save()
            return True
        except Exception as e:
            raise e

    

    def get_by_id(self, rol_id):
        try:
            data = Roles.objects.filter(id=rol_id, estado=True).first()
            if not data: raise Exception("Rol no encontrado")
            return data
        except Exception as e:
            raise e


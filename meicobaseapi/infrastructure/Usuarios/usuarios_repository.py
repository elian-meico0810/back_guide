from meicobaseapi.models import Usuarios
from django.db import connection
from django.db import transaction
from django.utils import timezone

class UsuariosRepository:
    def get_all(self):
        return Usuarios.objects.all()
    
    def get_by_email(self, email):
        return Usuarios.objects.get(correo=email)

    def create(self, data):
        return Usuarios.objects.create(**data)

    def update(self, usuario, nuevo_estado, auth_user):
        with transaction.atomic():
            if nuevo_estado is not None:
                usuario.estado = nuevo_estado
                usuario.updated_by = auth_user
                usuario.updated_at = timezone.now()
                usuario.save()

        return usuario

    def delete(self, user_id):
        user = Usuarios.objects.get(id=user_id)
        user.delete()

    
    def get_by_id(self, user_id):
        return Usuarios.objects.get(id=user_id)


from django.db import models

class Auditoria(models.Model):
    """Class representing a person"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, related_name='created_%(class)s_set')
    updated_by = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, related_name='updated_%(class)s_set')
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_%(class)s_set')

    class Meta:
        """Class representing a person"""
        abstract = True

class Usuarios(Auditoria):
    nombre = models.CharField(max_length=50)
    correo = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    celular = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'Usuarios'

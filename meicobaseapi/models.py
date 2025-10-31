from django.db import models

class Auditoria(models.Model):
    """Class representing a person"""
    created_at = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación")
    updated_at = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la última actualización")
    created_by = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, related_name='created_%(class)s_set', help_text="Usuario que creó el registro")
    updated_by = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, related_name='updated_%(class)s_set', help_text="Usuario que actualizó el registro")
    deleted_at = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora de eliminación")
    deleted_by = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_%(class)s_set', help_text="Usuario que eliminó el registro")

    class Meta:
        """Class representing a person"""
        abstract = True

class Usuarios(Auditoria):
    nombre = models.CharField(max_length=50, help_text="Nombre completo del usuario")
    correo = models.CharField(max_length=50, help_text="Correo electrónico del usuario")
    ciudad = models.CharField(max_length=50, null=True, blank=True, help_text="Ciudad del usuario")
    estado = models.BooleanField(default=True, help_text="Estado del usuario (activo/inactivo)")
    
    class Meta:
        db_table = 'Usuarios'

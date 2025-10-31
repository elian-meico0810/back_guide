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
        
        
class Roles(Auditoria):
    nombre = models.CharField(max_length=50, help_text="Nombre del rol")
    descripcion = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del rol")
    estado = models.BooleanField(default=True, help_text="Estado del rol (activo/inactivo)")
    
    class Meta:
        db_table = 'Roles'
        
        
class UsuarioRoles(Auditoria):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado al rol")
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, help_text="Rol asociado al usuario")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioRoles'
        
        
class Permisos(Auditoria):
    nombre = models.CharField(max_length=50, help_text="Nombre del permiso")
    codigo = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del permiso")
    estado = models.BooleanField(default=True, help_text="Estado del permiso (activo/inactivo)")
    
    class Meta:
        db_table = 'Permisos'
        
        
class RolPermisos(Auditoria):
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, help_text="Rol asociado al permiso")
    permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE, help_text="Permiso asociado al rol")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'RolPermisos'
        
        
class UsuarioPermisos(Auditoria):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado al permiso")
    permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE, help_text="Permiso asociado al usuario")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioPermisos'
        
class Bodegas(Auditoria):
    nombre = models.CharField(max_length=100, help_text="Nombre de la bodega")
    ciudad = models.CharField(max_length=255, null=True, blank=True, help_text="Ubicación de la bodega")
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción de la bodega")
    estado = models.BooleanField(default=True, help_text="Estado de la bodega (activo/inactivo)")
    
    class Meta:
        db_table = 'Bodegas'
        
class UsuarioBodegas(Auditoria):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado a la bodega")
    bodega = models.ForeignKey(Bodegas, on_delete=models.CASCADE, help_text="Bodega asociada al usuario")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioBodegas'

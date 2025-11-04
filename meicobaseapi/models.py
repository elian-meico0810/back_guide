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
        default_permissions=()        
        
class Roles(Auditoria):
    nombre = models.CharField(max_length=50, help_text="Nombre del rol")
    descripcion = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del rol")
    estado = models.BooleanField(default=True, help_text="Estado del rol (activo/inactivo)")
    
    class Meta:
        db_table = 'Roles'
        default_permissions=()        
        
        
class UsuarioRoles(Auditoria):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado al rol")
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, help_text="Rol asociado al usuario")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioRoles'
        default_permissions=()        
       
        
class Permisos(Auditoria):
    nombre = models.CharField(max_length=50, help_text="Nombre del permiso")
    codigo = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del permiso")
    estado = models.BooleanField(default=True, help_text="Estado del permiso (activo/inactivo)")
    
    class Meta:
        db_table = 'Permisos'
        default_permissions=()        
        
        
class RolPermisos(Auditoria):
    rol = models.ForeignKey(Roles, on_delete=models.CASCADE, help_text="Rol asociado al permiso")
    permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE, help_text="Permiso asociado al rol")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'RolPermisos'
        default_permissions=()        
        
        
class UsuarioPermisos(Auditoria):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado al permiso")
    permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE, help_text="Permiso asociado al usuario")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioPermisos'
        default_permissions=()        
       
       
class Bodegas(Auditoria):
    nombre = models.CharField(max_length=100, help_text="Nombre de la bodega")
    ciudad = models.CharField(max_length=255, null=True, blank=True, help_text="Ubicación de la bodega")
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción de la bodega")
    estado = models.BooleanField(default=True, help_text="Estado de la bodega (activo/inactivo)")
    
    class Meta:
        db_table = 'Bodegas'
        default_permissions=()        


class UsuarioBodegas(Auditoria):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado a la bodega")
    bodega = models.ForeignKey(Bodegas, on_delete=models.CASCADE, help_text="Bodega asociada al usuario")
    estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioBodegas'
        default_permissions=()        


class Parametros(Auditoria):
    nombre = models.CharField(max_length=100, help_text="Clave del parámetro")
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción del parámetro")
    estado = models.BooleanField(default=True, help_text="Estado del parámetro (activo/inactivo)")
    
    class Meta:
        db_table = 'Parametros'
        default_permissions=()        


class Atributos(Auditoria):
    nombre = models.CharField(max_length=100, help_text="Nombre del atributo")
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción del atributo")
    estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")
    parametro = models.ForeignKey(Parametros, on_delete=models.CASCADE, help_text="Parámetro asociado al atributo")
    
    class Meta:
        db_table = 'Atributos'
        default_permissions=()        

        
class Documentos(Auditoria):
    numero_documento = models.CharField(max_length=100, help_text="Nombre del documento")
    tipo_documento = models.CharField(max_length=255, help_text="Tipo de documento asociado al atributo", blank=True, null=True)
    aplica = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del documento")
    valor = models.CharField(max_length=255, null=False, help_text="Valor del documento")
    fecha = models.CharField(max_length=50, null=False, help_text="Fecha del documento")
    drf_antes_descuento = models.CharField(max_length=50, null=True, blank=True, help_text="DRF antes de descuento")
    drf_real = models.CharField(max_length=50, null=True, blank=True, help_text="DRF real")
    cantidad_cargada = models.CharField(max_length=50, null=True, blank=True, help_text="Cantidad cargada")
    estado = models.BooleanField(default=True, help_text="Estado del documento (activo/inactivo)")
    cantidad_reacudada = models.CharField(max_length=50, null=True, blank=True, help_text="Cantidad recaudada")
    diferencia = models.CharField(max_length=50, null=True, blank=True, help_text="Diferencia entre cantidad cargada y recaudada")
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del cliente asociado al documento")
    estado_documento = models.CharField(max_length=100, null=True, blank=True, help_text="Estado del documento")
    descripcion = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción adicional del documento")
    
    class Meta:
        db_table = 'Documentos'
        default_permissions=()        

        
class DocumentosAuditoria(Auditoria):
    documento = models.ForeignKey(Documentos, on_delete=models.CASCADE, help_text="Documento asociado a la auditoría")
    numero_documento = models.CharField(max_length=100, help_text="Nombre del documento")
    tipo_documento = models.CharField(max_length=255, help_text="Tipo de documento asociado al atributo", blank=True, null=True)
    aplica = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del documento")
    valor = models.CharField(max_length=255, null=False, help_text="Valor del documento")
    fecha = models.CharField(max_length=50, null=False, help_text="Fecha del documento")
    drf_antes_descuento = models.CharField(max_length=50, null=True, blank=True, help_text="DRF antes de descuento")
    drf_real = models.CharField(max_length=50, null=True, blank=True, help_text="DRF real")
    cantidad_cargada = models.CharField(max_length=50, null=True, blank=True, help_text="Cantidad cargada")
    estado = models.BooleanField(default=True, help_text="Estado del documento (activo/inactivo)")
    cantidad_reacudada = models.CharField(max_length=50, null=True, blank=True, help_text="Cantidad recaudada")
    diferencia = models.CharField(max_length=50, null=True, blank=True, help_text="Diferencia entre cantidad cargada y recaudada")
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del cliente asociado al documento")
    estado_documento = models.CharField(max_length=100, null=True, blank=True, help_text="Estado del documento")
    descripcion = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción adicional del documento")
    
    class Meta:
        db_table = 'DocumentosAuditoria'
        default_permissions=()        
        
        
class Guias(Auditoria):
    numero_guia = models.CharField(max_length=100, help_text="Número de la guía")
    descripcion = models.TextField(null=True, blank=True, help_text="Descripción de la guía")
    estado = models.BooleanField(default=True, help_text="Estado de la guía (activo/inactivo)")
    fecha_creacion_guia = models.CharField(max_length=50, null=False, help_text="Fecha de creación de la guía")
    fecha_despacho_guia = models.CharField(max_length=50, null=False, help_text="Fecha de despacho de la guía")
    tipo_guia = models.CharField(max_length=100, help_text="Tipo de guía")
    id_bodega = models.CharField(max_length=255, null=True, blank=True, help_text="Bodega asociada a la guía")
    tipo_id_propietario_transporte = models.CharField(max_length=50, null=True, blank=True, help_text="Tipo de identificación del propietario del transporte")
    id_propietario_transporte = models.CharField(max_length=50, null=True, blank=True, help_text="Identificación del propietario del transporte")
    nombre_propietario_transporte = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del propietario del transporte")
    placa = models.CharField(max_length=20, null=True, blank=True, help_text="Placa del vehículo de transporte")
    tipo_id_conductor = models.CharField(max_length=50, null=True, blank=True, help_text="Tipo de identificación del conductor")
    nombre_conductor = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del conductor")
    estado_guia_original = models.CharField(max_length=100, null=True, blank=True, help_text="Estado original de la guía")
    estado_guia = models.CharField(max_length=100, null=True, blank=True, help_text="Estado actual de la guía")
    nombre_bodega = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre de la bodega asociada a la guía")
    cantidad_facturas = models.IntegerField(null=True, blank=True, help_text="Cantidad de facturas en la guía")
    fecha_promesa = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha promesa de entrega de la guía")
    fecha_retorno = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de retorno de la guía")
    valor_reacaudar = models.CharField(max_length=50, null=True, blank=True, help_text="Valor a recaudar en la guía")
    id_usuario = models.IntegerField(null=True, blank=True, help_text="ID del usuario asociado a la guía")
    nombre_usuario = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario asociado a la guía")
        
    class Meta:
        db_table = 'Guias'
        default_permissions=()
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

        
class PlanillaEncabezado(Auditoria):
    planilla_enc_id = models.AutoField(primary_key=True, help_text="ID de la planilla")
    fecha_creacion_planilla = models.DateTimeField(null=True, blank=True, help_text="Fecha de creación de la planilla")
    usuario_creacion_planilla = models.CharField(max_length=255, null=True, blank=True, help_text="Usuario que creó la planilla")
    total_esperado_recaudar = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total esperado a recaudar")
    total_recaudado = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total recaudado")
    total_diferencia = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total diferencia entre esperado y recaudado")
    cantidad_guias_despachadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías despachadas")
    cantidad_guias_confirmadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías confirmadas")

    class Meta:
        db_table = 'PlanillaEncabezado'
        default_permissions = ()
        
        
class PlanillaEncabezadoAuditoria(Auditoria):
    planilla_enc_id = models.AutoField(primary_key=True, help_text="ID de la planilla")
    fecha_creacion_planilla = models.DateTimeField(null=True, blank=True, help_text="Fecha de creación de la planilla")
    usuario_creacion_planilla = models.CharField(max_length=255, null=True, blank=True, help_text="Usuario que creó la planilla")
    total_esperado_recaudar = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total esperado a recaudar")
    total_recaudado = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total recaudado")
    total_diferencia = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total diferencia entre esperado y recaudado")
    cantidad_guias_despachadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías despachadas")
    cantidad_guias_confirmadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías confirmadas")
    planilla_encabezado= models.ForeignKey(PlanillaEncabezado, on_delete=models.CASCADE, help_text="Referencia a la planilla encabezado original")
    
    class Meta:
        db_table = 'PlanillaEncabezadoAuditoria'
        default_permissions = ()
        
        
class PlanillaDetalles(Auditoria):
    planilla_enc_id = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    numero_guia = models.IntegerField(null=True, blank=True, help_text="Número de la guía asociada a la planilla")
    fecha_creacion_guia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de creación de la guía")
    fecha_despacho_guia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de despacho de la guía")
    tipo_guia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    bodega_id = models.CharField(max_length=100, null=True, blank=True, help_text="Identificador de la bodega")
    tipo_id_propietario_transportador = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de ID del propietario o transportador (Cédula o NIT)")
    id_propietario_transportador = models.CharField(max_length=100, null=True, blank=True, help_text="ID del propietario o transportador")
    nombre_propietario_transportador = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del propietario o transportador")
    placa = models.CharField(max_length=50, null=True, blank=True, help_text="Placa del vehículo")
    tipo_id_conductor = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de identificación del conductor (Cédula o NIT)")
    conductor_id = models.CharField(max_length=100, null=True, blank=True, help_text="ID del conductor")
    nombre_conductor = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del conductor")
    estado_guia_original = models.CharField(max_length=100, null=True, blank=True, help_text="Estado original de la guía (CERRADA/IMPRESA)")
    estado_guia = models.CharField(max_length=100, null=True, blank=True, help_text="Estado actual de la guía (DESPACHADA/CONFIRMADA)")
    cantidad_facturas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de facturas asociadas")
    fecha_promesa = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de promesa")
    fecha_retorno = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de retorno")
    valor_recaudar = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Valor a recaudar")
    usuario_id_ingreso = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó el ingreso")
    nombre_usuario_ingreso = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó el ingreso")
    correo_usuario_ingreso = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó el ingreso")
    usuario_id_confirmacion = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó la confirmación")
    nombre_usuario_confirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó la confirmación")
    correo_usuario_confirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó la confirmación")
    fecha_ingreso_corta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de ingreso (yyyymmdd)")
    fecha_ingreso_full = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de ingreso (datetime)")
    fecha_confirmacion_corta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de confirmación (yyyymmdd)")
    fecha_confirmacion_full = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de confirmación (datetime)")

    class Meta:
        db_table = 'PlanillaDetalles'
        default_permissions = ()


class PlanillaDetallesAuditoria(Auditoria):
    planilla_enc_id = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    numero_guia = models.IntegerField(null=True, blank=True, help_text="Número de la guía asociada a la planilla")
    fecha_creacion_guia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de creación de la guía")
    fecha_despacho_guia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de despacho de la guía")
    tipo_guia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    bodega_id = models.CharField(max_length=100, null=True, blank=True, help_text="Identificador de la bodega")
    tipo_id_propietario_transportador = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de ID del propietario o transportador (Cédula o NIT)")
    id_propietario_transportador = models.CharField(max_length=100, null=True, blank=True, help_text="ID del propietario o transportador")
    nombre_propietario_transportador = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del propietario o transportador")
    placa = models.CharField(max_length=50, null=True, blank=True, help_text="Placa del vehículo")
    tipo_id_conductor = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de identificación del conductor (Cédula o NIT)")
    conductor_id = models.CharField(max_length=100, null=True, blank=True, help_text="ID del conductor")
    nombre_conductor = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del conductor")
    estado_guia_original = models.CharField(max_length=100, null=True, blank=True, help_text="Estado original de la guía (CERRADA/IMPRESA)")
    estado_guia = models.CharField(max_length=100, null=True, blank=True, help_text="Estado actual de la guía (DESPACHADA/CONFIRMADA)")
    cantidad_facturas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de facturas asociadas")
    fecha_promesa = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de promesa")
    fecha_retorno = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de retorno")
    valor_recaudar = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Valor a recaudar")
    usuario_id_ingreso = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó el ingreso")
    nombre_usuario_ingreso = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó el ingreso")
    correo_usuario_ingreso = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó el ingreso")
    usuario_id_confirmacion = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó la confirmación")
    nombre_usuario_confirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó la confirmación")
    correo_usuario_confirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó la confirmación")
    fecha_ingreso_corta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de ingreso (yyyymmdd)")
    fecha_ingreso_full = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de ingreso (datetime)")
    fecha_confirmacion_corta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de confirmación (yyyymmdd)")
    fecha_confirmacion_full = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de confirmación (datetime)")
    planilla_detalle = models.ForeignKey(PlanillaDetalles, on_delete=models.CASCADE, help_text="Referencia a la planilla detalles original")
    
    class Meta:
        db_table = 'PlanillaDetalleAuditoria'
        default_permissions = ()
        
        
class PlanillaDetalleFactura(Auditoria):
    planilla_enc_id = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    numero_guia = models.IntegerField(null=True, blank=True, help_text="Número de guía asociado")
    numero_documento = models.CharField(max_length=50, null=True, blank=True, help_text="Número de documento (factura)")
    tipo_documento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista)")
    valor_factura = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor total de la factura")
    valor_devolucion = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor de la devolución")
    valor_esperado_recaudar = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor esperado a recaudar")
    valor_recaudado = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor efectivamente recaudado")
    diferencia = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Diferencia entre lo esperado y lo recaudado")

    class Meta:
        db_table = 'PlanillaDetalleFactura'
        default_permissions = ()
        
        
class PlanillaDetalleFacturaAuditoria(Auditoria):
    planilla_enc_id = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    numero_guia = models.IntegerField(null=True, blank=True, help_text="Número de guía asociado")
    numero_documento = models.CharField(max_length=50, null=True, blank=True, help_text="Número de documento (factura)")
    tipo_documento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista)")
    valor_factura = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor total de la factura")
    valor_devolucion = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor de la devolución")
    valor_esperado_recaudar = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor esperado a recaudar")
    valor_recaudado = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor efectivamente recaudado")
    diferencia = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Diferencia entre lo esperado y lo recaudado")
    planilla_detalle = models.ForeignKey(PlanillaDetalleFactura, on_delete=models.CASCADE, help_text="Referencia a la planilla detalles facuras original")
    
    class Meta:
        db_table = 'PlanillaDetalleFacturaAuditoria'
        default_permissions = ()
        

class Documentos(Auditoria):
    numero_documento = models.CharField(max_length=50, null=True, blank=True, help_text="Número del documento")
    tipo_documento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista, C: Nota_Credito)")
    valor_documento = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor total del documento")
    fecha_documento = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha del documento")
    aplica_a = models.CharField(max_length=50, null=True, blank=True, help_text="Documento al que aplica (si es nota crédito)")
    bodega_id = models.CharField(max_length=50, null=True, blank=True, help_text="Identificador de la bodega")
    nombre_bodega = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre de la bodega")
    codigo_cliente = models.CharField(max_length=50, null=True, blank=True, help_text="Código del cliente asociado")
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del cliente asociado")
    condicion_pago = models.CharField(max_length=100, null=True, blank=True, help_text="Condición de pago del documento")

    class Meta:
        db_table = 'Documentos'
        default_permissions = ()
        
        
class DocumentosAuditoria(Auditoria):
    numero_documento = models.CharField(max_length=50, null=True, blank=True, help_text="Número del documento")
    tipo_documento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista, C: Nota_Credito)")
    valor_documento = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True, help_text="Valor total del documento")
    fecha_documento = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha del documento")
    aplica_a = models.CharField(max_length=50, null=True, blank=True, help_text="Documento al que aplica (si es nota crédito)")
    bodega_id = models.CharField(max_length=50, null=True, blank=True, help_text="Identificador de la bodega")
    nombre_bodega = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre de la bodega")
    codigo_cliente = models.CharField(max_length=50, null=True, blank=True, help_text="Código del cliente asociado")
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del cliente asociado")
    condicion_pago = models.CharField(max_length=100, null=True, blank=True, help_text="Condición de pago del documento")
    documento = models.ForeignKey(Documentos, on_delete=models.CASCADE, help_text="Referencia al documento original")
    
    class Meta:
        db_table = 'DocumentosAuditoria'
        default_permissions = ()
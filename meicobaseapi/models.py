from django.db import models
from django.db.models.signals import post_save

from meicobaseapi.core.helpers.utils import model_to_dict


class Auditoria(models.Model):
    """Class representing a person"""
    id = models.BigAutoField(primary_key=True, help_text="Hace referencia al id auto-incremental.")
    CreatedAt = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación")
    UpdatedAt = models.DateTimeField(auto_now=True, help_text="Fecha y hora de la última actualización")
    CreatedBy = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, related_name='created_%(class)s_set', help_text="Usuario que creó el registro")
    UpdatedBy = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, related_name='updated_%(class)s_set', help_text="Usuario que actualizó el registro")
    DeletedAt = models.DateTimeField(null=True, blank=True, help_text="Fecha y hora de eliminación")
    DeletedBy = models.ForeignKey('Usuarios', on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_%(class)s_set', help_text="Usuario que eliminó el registro")

    class Meta:
        """Class representing a person"""
        abstract = True


class Usuarios(Auditoria):
    Nombre = models.CharField(max_length=50, help_text="Nombre completo del usuario")
    Correo = models.CharField(max_length=50, help_text="Correo electrónico del usuario")
    Ciudad = models.CharField(max_length=50, null=True, blank=True, help_text="Ciudad del usuario")
    Estado = models.BooleanField(default=True, help_text="Estado del usuario (activo/inactivo)")
    
    class Meta:
        db_table = 'Usuarios'
        default_permissions=()        
        
        
class Roles(Auditoria):
    Nombre = models.CharField(max_length=50, help_text="Nombre del rol")
    Descripcion = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del rol")
    Estado = models.BooleanField(default=True, help_text="Estado del rol (activo/inactivo)")
    
    class Meta:
        db_table = 'Roles'
        default_permissions=()        
        
        
class UsuarioRoles(Auditoria):
    Usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado al rol")
    Rol = models.ForeignKey(Roles, on_delete=models.CASCADE, help_text="Rol asociado al usuario")
    Estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioRoles'
        default_permissions=()        
       
        
class Permisos(Auditoria):
    Nombre = models.CharField(max_length=50, help_text="Nombre del permiso")
    Codigo = models.CharField(max_length=255, null=True, blank=True, help_text="Descripción del permiso")
    Estado = models.BooleanField(default=True, help_text="Estado del permiso (activo/inactivo)")
    
    class Meta:
        db_table = 'Permisos'
        default_permissions=()        
        
        
class RolPermisos(Auditoria):
    Rol = models.ForeignKey(Roles, on_delete=models.CASCADE, help_text="Rol asociado al permiso")
    Permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE, help_text="Permiso asociado al rol")
    Estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'RolPermisos'
        default_permissions=()        
        
        
class UsuarioPermisos(Auditoria):
    Usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado al permiso")
    Permiso = models.ForeignKey(Permisos, on_delete=models.CASCADE, help_text="Permiso asociado al usuario")
    Estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioPermisos'
        default_permissions=()        
       
       
class Bodegas(Auditoria):
    Nombre = models.CharField(max_length=100, help_text="Nombre de la bodega")
    Ciudad = models.CharField(max_length=255, null=True, blank=True, help_text="Ubicación de la bodega")
    Descripcion = models.TextField(null=True, blank=True, help_text="Descripción de la bodega")
    Estado = models.BooleanField(default=True, help_text="Estado de la bodega (activo/inactivo)")
    
    class Meta:
        db_table = 'Bodegas'
        default_permissions=()        


class UsuarioBodegas(Auditoria):
    Usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, help_text="Usuario asociado a la bodega")
    Bodega = models.ForeignKey(Bodegas, on_delete=models.CASCADE, help_text="Bodega asociada al usuario")
    Estado = models.BooleanField(default=True, help_text="Estado de la asociación (activo/inactivo)")
    
    class Meta:
        db_table = 'UsuarioBodegas'
        default_permissions=()        


class Parametros(Auditoria):
    Nombre = models.CharField(max_length=100, help_text="Clave del parámetro")
    Descripcion = models.TextField(null=True, blank=True, help_text="Descripción del parámetro")
    Estado = models.BooleanField(default=True, help_text="Estado del parámetro (activo/inactivo)")
    
    class Meta:
        db_table = 'Parametros'
        default_permissions=()        


class Atributos(Auditoria):
    Nombre = models.CharField(max_length=100, help_text="Nombre del atributo")
    Descripcion = models.TextField(null=True, blank=True, help_text="Descripción del atributo")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")
    Parametro = models.ForeignKey(Parametros, on_delete=models.CASCADE, help_text="Parámetro asociado al atributo")
    
    class Meta:
        db_table = 'Atributos'
        default_permissions=()        

        
class PlanillaEncabezado(Auditoria):
    PlanillaEncId = models.IntegerField( null=True, blank=True, help_text="ID del encabezado de la planilla")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    TipoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    FechaCreacionPlanilla = models.DateTimeField(null=True, blank=True, help_text="Fecha de creación de la planilla")
    UsuarioCreacionPlanilla = models.CharField(max_length=255, null=True, blank=True, help_text="Usuario que creó la planilla")
    TotalEsperadoRecaudar = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total esperado a recaudar")
    TotalRecaudado = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total recaudado")
    TotalDiferencia = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total diferencia entre esperado y recaudado")
    CantidadGuiasDespachadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías despachadas")
    CantidadGuiasConfirmadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías confirmadas")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")

    class Meta:
        db_table = 'PlanillaEncabezado'
        default_permissions = ()
        
# ====================== AUDITORIA INTERNA ======================================
def planilla_encabezado_post_save(sender, instance, created, *args, **kwargs):
        model_dict = model_to_dict(instance,
        foreign_keys=[
           
        ])
        model_dict.pop('model')
        model_dict['PlanillaEncabezadoId'] = model_dict.pop('pk')
        PlanillaEncabezadoAuditoria.objects.create(**model_dict)

post_save.connect(planilla_encabezado_post_save,sender=PlanillaEncabezado)
        
class PlanillaEncabezadoAuditoria(Auditoria):
    PlanillaEncId = models.IntegerField( null=True, blank=True, help_text="ID del encabezado de la planilla")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    TipoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    FechaCreacionPlanilla = models.DateTimeField(null=True, blank=True, help_text="Fecha de creación de la planilla")
    UsuarioCreacionPlanilla = models.CharField(max_length=255, null=True, blank=True, help_text="Usuario que creó la planilla")
    TotalEsperadoRecaudar = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total esperado a recaudar")
    TotalRecaudado = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total recaudado")
    TotalDiferencia = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Total diferencia entre esperado y recaudado")
    CantidadGuiasDespachadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías despachadas")
    CantidadGuiasConfirmadas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de guías confirmadas")
    PlanillaEncabezadoId =  models.IntegerField(null=True, blank=True, help_text="Referencia a la planilla encabezado original")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")

    class Meta:
        db_table = 'PlanillaEncabezadoAuditoria'
        default_permissions = ()

        
class PlanillaDetalles(Auditoria):
    PlanillaEncId = models.IntegerField( null=True, blank=True, help_text="ID del encabezado de la planilla")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    FechaCreacionGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de creación de la guía")
    FechaDespachoGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de despacho de la guía")
    TipoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    BodegaId = models.CharField(max_length=100, null=True, blank=True, help_text="Identificador de la bodega")
    TipoIdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de ID del propietario o transportador (Cédula o NIT)")
    IdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="ID del propietario o transportador")
    NombrePropietarioTransportador = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del propietario o transportador")
    Placa = models.CharField(max_length=50, null=True, blank=True, help_text="Placa del vehículo")
    TipoIdConductor = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de identificación del conductor (Cédula o NIT)")
    ConductorId = models.CharField(max_length=100, null=True, blank=True, help_text="ID del conductor")
    NombreConductor = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del conductor")
    EstadoGuiaOriginal = models.CharField(max_length=100, null=True, blank=True, help_text="Estado original de la guía (CERRADA/IMPRESA)")
    EstadoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Estado actual de la guía (DESPACHADA/CONFIRMADA)")
    CantidadFacturas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de facturas asociadas")
    FechaPromesa = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de promesa")
    FechaRetorno = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de retorno")
    ValorRecaudar = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor a recaudar")
    UsuarioIdIngreso = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó el ingreso")
    NombreUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó el ingreso")
    CorreoUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó el ingreso")
    UsuarioIdConfirmacion = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó la confirmación")
    NombreUsuarioConfirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó la confirmación")
    CorreoUsuarioConfirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó la confirmación")
    FechaIngresoCorta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de ingreso (yyyymmdd)")
    FechaIngresoFull = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de ingreso (datetime)")
    FechaConfirmacionCorta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de confirmación (yyyymmdd)")
    FechaConfirmacionFull = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de confirmación (datetime)")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")

    class Meta:
        db_table = 'PlanillaDetalles'
        default_permissions = ()

# ====================== AUDITORIA INTERNA ======================================
def planilla_detalle_post_save(sender, instance, created, *args, **kwargs):
        model_dict = model_to_dict(instance,
        foreign_keys=[
           
        ])
        model_dict.pop('model')
        model_dict['PlanillaDetalleId'] = model_dict.pop('pk')
        PlanillaDetallesAuditoria.objects.create(**model_dict)

post_save.connect(planilla_detalle_post_save,sender=PlanillaDetalles)


class PlanillaDetallesAuditoria(Auditoria):
    PlanillaEncId = models.IntegerField( null=True, blank=True, help_text="ID del encabezado de la planilla")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    FechaCreacionGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de creación de la guía")
    FechaDespachoGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de despacho de la guía")
    TipoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    BodegaId = models.CharField(max_length=100, null=True, blank=True, help_text="Identificador de la bodega")
    TipoIdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de ID del propietario o transportador (Cédula o NIT)")
    IdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="ID del propietario o transportador")
    NombrePropietarioTransportador = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del propietario o transportador")
    Placa = models.CharField(max_length=50, null=True, blank=True, help_text="Placa del vehículo")
    TipoIdConductor = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de identificación del conductor (Cédula o NIT)")
    ConductorId = models.CharField(max_length=100, null=True, blank=True, help_text="ID del conductor")
    NombreConductor = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del conductor")
    EstadoGuiaOriginal = models.CharField(max_length=100, null=True, blank=True, help_text="Estado original de la guía (CERRADA/IMPRESA)")
    EstadoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Estado actual de la guía (DESPACHADA/CONFIRMADA)")
    CantidadFacturas = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, help_text="Cantidad de facturas asociadas")
    FechaPromesa = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de promesa")
    FechaRetorno = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de retorno")
    ValorRecaudar = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor a recaudar")
    UsuarioIdIngreso = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó el ingreso")
    NombreUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó el ingreso")
    CorreoUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó el ingreso")
    UsuarioIdConfirmacion = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó la confirmación")
    NombreUsuarioConfirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó la confirmación")
    CorreoUsuarioConfirmacion = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó la confirmación")
    FechaIngresoCorta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de ingreso (yyyymmdd)")
    FechaIngresoFull = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de ingreso (datetime)")
    FechaConfirmacionCorta = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha de confirmación (yyyymmdd)")
    FechaConfirmacionFull = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha completa de confirmación (datetime)")
    PlanillaDetalleId = models.IntegerField(null=True, blank=True, help_text="Referencia a la planilla detalles original")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")
 
    class Meta:
        db_table = 'PlanillaDetalleAuditoria'
        default_permissions = ()
        
        
class PlanillaDetalleFactura(Auditoria):
    PlanillaEncId = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    BodegaId = models.CharField(max_length=50, null=True, blank=True, help_text="Hace referencia al id de las bodegas.")
    FechaCreacionGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de creación de la guía")
    FechaDespachoGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de despacho de la guía")
    TipoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    TipoIdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de ID del propietario o transportador (Cédula o NIT)")
    IdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="ID del propietario o transportador")
    NombrePropietarioTransportador = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del propietario o transportador")
    Placa = models.CharField(max_length=50, null=True, blank=True, help_text="Placa del vehículo")
    TipoIdConductor = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de identificación del conductor (Cédula o NIT)")
    ConductorId = models.CharField(max_length=100, null=True, blank=True, help_text="ID del conductor")
    NombreConductor = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del conductor")
    EstadoGuiaOriginal = models.CharField(max_length=100, null=True, blank=True, help_text="Estado original de la guía (CERRADA/IMPRESA)")
    EstadoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Estado actual de la guía (DESPACHADA/CONFIRMADA)")
    FechaPromesa = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de promesa")
    FechaRetorno = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de retorno")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    NumeroDocumento = models.CharField(max_length=50, null=True, blank=True, help_text="Número de documento (factura)")
    TipoDocumento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista)")
    CodigoCliente = models.CharField(max_length=50, null=True, blank=True, help_text="Código del cliente asociado")
    RazonSocialCliente = models.CharField(max_length=255, null=True, blank=True, help_text="Razon socail del cliente ")
    ValorDevolucion = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de la devolución")
    ValorFactura = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de la factura")
    DfrFactura = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Diferencia de facturas")
    NumerosNc  = models.CharField(max_length=2000, null=True, blank=True, help_text="Numero de nota cerdito")
    ValorNc = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de nota credito")
    DfrReal = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Diferencia real")
    ValorEsperadoRecaudar = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor esperado a recaudar")
    ValorRecaudado = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor efectivamente recaudado")
    Diferencia = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Diferencia entre lo esperado y lo recaudado")
    EstadoPlanilla = models.CharField(max_length=255, null=True, blank=True, help_text="Estado del usuario (activo/inactivo)")
    CodigoCondicionPago = models.CharField(max_length=255, null=True, blank=True, help_text="codigo condicion pago")
    NombreCondicionPago = models.CharField(max_length=255, null=True, blank=True, help_text="nombre condicion pago")
    UsuarioIdIngreso = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó el ingreso")
    NombreUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó el ingreso")
    CorreoUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó el ingreso")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")

    class Meta:
        db_table = 'PlanillaDetalleFactura'
        default_permissions = ()
        
# ====================== AUDITORIA INTERNA ======================================
def planilla_detalle_facturas_post_save(sender, instance, created, *args, **kwargs):
        model_dict = model_to_dict(instance,
        foreign_keys=[
           
        ])
        model_dict.pop('model')
        model_dict['PlanillaDetalleId'] = model_dict.pop('pk')
        PlanillaDetalleFacturaAuditoria.objects.create(**model_dict)

post_save.connect(planilla_detalle_facturas_post_save,sender=PlanillaDetalleFactura)

        
class PlanillaDetalleFacturaAuditoria(Auditoria):
    PlanillaEncId = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    BodegaId = models.CharField(max_length=50, null=True, blank=True, help_text="Hace referencia al id de las bodegas.")
    FechaCreacionGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de creación de la guía")
    FechaDespachoGuia = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de despacho de la guía")
    TipoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de guía (MIXTA, TAT, MAYORISTA)")
    TipoIdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de ID del propietario o transportador (Cédula o NIT)")
    IdPropietarioTransportador = models.CharField(max_length=100, null=True, blank=True, help_text="ID del propietario o transportador")
    NombrePropietarioTransportador = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del propietario o transportador")
    Placa = models.CharField(max_length=50, null=True, blank=True, help_text="Placa del vehículo")
    TipoIdConductor = models.CharField(max_length=100, null=True, blank=True, help_text="Tipo de identificación del conductor (Cédula o NIT)")
    ConductorId = models.CharField(max_length=100, null=True, blank=True, help_text="ID del conductor")
    NombreConductor = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del conductor")
    EstadoGuiaOriginal = models.CharField(max_length=100, null=True, blank=True, help_text="Estado original de la guía (CERRADA/IMPRESA)")
    EstadoGuia = models.CharField(max_length=100, null=True, blank=True, help_text="Estado actual de la guía (DESPACHADA/CONFIRMADA)")
    FechaPromesa = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de promesa")
    FechaRetorno = models.CharField(max_length=255, null=True, blank=True, help_text="Fecha de retorno")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    NumeroDocumento = models.CharField(max_length=50, null=True, blank=True, help_text="Número de documento (factura)")
    TipoDocumento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista)")
    CodigoCliente = models.CharField(max_length=50, null=True, blank=True, help_text="Código del cliente asociado")
    RazonSocialCliente = models.CharField(max_length=255, null=True, blank=True, help_text="Razon socail del cliente ")
    ValorDevolucion = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de la devolución")
    ValorFactura = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de la factura")
    DfrFactura = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Diferencia de facturas")
    NumerosNc  = models.CharField(max_length=2000, null=True, blank=True, help_text="Numero de nota cerdito")
    ValorNc = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de nota credito")
    DfrReal = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Diferencia real")
    ValorEsperadoRecaudar = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor esperado a recaudar")
    ValorRecaudado = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor efectivamente recaudado")
    Diferencia = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Diferencia entre lo esperado y lo recaudado")
    EstadoPlanilla = models.CharField(max_length=255, null=True, blank=True, help_text="Estado del usuario (activo/inactivo)")
    CodigoCondicionPago = models.CharField(max_length=255, null=True, blank=True, help_text="codigo condicion pago")
    NombreCondicionPago = models.CharField(max_length=255, null=True, blank=True, help_text="nombre condicion pago")
    UsuarioIdIngreso = models.CharField(max_length=100, null=True, blank=True, help_text="ID del usuario que realizó el ingreso")
    NombreUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del usuario que realizó el ingreso")
    CorreoUsuarioIngreso = models.CharField(max_length=255, null=True, blank=True, help_text="Correo del usuario que realizó el ingreso")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")
    PlanillaDetalleId =models.IntegerField(null=True, blank=True, help_text="Referencia a la planilla detalles facuras original")

    class Meta:
        db_table = 'PlanillaDetalleFacturaAuditoria'
        default_permissions = ()
        

class Documentos(Auditoria):
    PlanillaEncId = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    NumeroDocumento = models.CharField(max_length=50, null=True, blank=True, help_text="Número del documento")
    TipoDocumento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista, C: Nota_Credito)")
    ValorDocumento = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor total del documento")
    FechaDocumento = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha del documento")
    AplicaA = models.CharField(max_length=50, null=True, blank=True, help_text="Documento al que aplica (si es nota crédito)")
    BodegaId = models.CharField(max_length=50, null=True, blank=True, help_text="Identificador de la bodega")
    NombreBodega = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre de la bodega")
    CodigoCliente = models.CharField(max_length=50, null=True, blank=True, help_text="Código del cliente asociado")
    NombreCliente = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del cliente asociado")
    CondicionPago = models.CharField(max_length=100, null=True, blank=True, help_text="Condición de pago del documento")
    NombreCondicionPago = models.CharField(max_length=100, null=True, blank=True, help_text="Nombre de condición de pago del documento")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")

    class Meta:
        db_table = 'Documentos'
        default_permissions = ()
        
# ====================== AUDITORIA INTERNA ======================================
def documentos_post_save(sender, instance, created, *args, **kwargs):
        model_dict = model_to_dict(instance,
        foreign_keys=[
           
        ])
        model_dict.pop('model')
        model_dict['DocumentoId'] = model_dict.pop('pk')
        DocumentosAuditoria.objects.create(**model_dict)

post_save.connect(documentos_post_save,sender=Documentos)

        
class DocumentosAuditoria(Auditoria):
    PlanillaEncId = models.IntegerField(null=True, blank=True, help_text="ID del encabezado de la planilla")
    IdGoAnyWhere = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referncia al id de GoAnyWhere")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    NumeroDocumento = models.CharField(max_length=50, null=True, blank=True, help_text="Número del documento")
    TipoDocumento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de documento (I: Factura_TAT, O: Factura_Mayorista, C: Nota_Credito)")
    ValorDocumento = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor total del documento")
    FechaDocumento = models.CharField(max_length=50, null=True, blank=True, help_text="Fecha del documento")
    AplicaA = models.CharField(max_length=50, null=True, blank=True, help_text="Documento al que aplica (si es nota crédito)")
    BodegaId = models.CharField(max_length=50, null=True, blank=True, help_text="Identificador de la bodega")
    NombreBodega = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre de la bodega")
    CodigoCliente = models.CharField(max_length=50, null=True, blank=True, help_text="Código del cliente asociado")
    NombreCliente = models.CharField(max_length=255, null=True, blank=True, help_text="Nombre del cliente asociado")
    CondicionPago = models.CharField(max_length=100, null=True, blank=True, help_text="Condición de pago del documento")
    NombreCondicionPago = models.CharField(max_length=100, null=True, blank=True, help_text="Nombre de condición de pago del documento")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")
    DocumentoId = models.IntegerField(null=True, blank=True, help_text="Referencia al documento original")
    
    class Meta:
        db_table = 'DocumentosAuditoria'
        default_permissions = ()
        
        
class Consignaciones(Auditoria):
    NumeroPlanilla = models.IntegerField(null=True, blank=True, help_text="ID de la planilla")
    TipoConsignacion = models.CharField(max_length=255, null=True, blank=True,help_text="Tipo de consignacion.")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    NumeroDocumento = models.CharField(max_length=255, null=True, blank=True,help_text="Número de documento o factura")
    NumeroConsignacion  = models.IntegerField(null=True, blank=True, help_text="Número de consignacion (Id auto-incremental)")
    NumeroConsignacionBanco  = models.CharField(max_length=255, null=True, blank=True, help_text="Número de consignacion banco")
    FechaRegistroCorta = models.CharField(max_length=100, null=True, blank=True, help_text="Fecha de registro yyyymmdd")
    FechaConsignacionCorta = models.CharField(max_length=100, null=True, blank=True, help_text="Fecha de consignacion yyyymmdd")
    FechaRegistroFull = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación yyyymmdd hh:mm:ss")
    FechaConsignacionFull = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación yyyymmdd hh:mm:ss")
    ValorConsignacion = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de la consignacion")
    RutaArchivoSoporte = models.TextField(null=True, blank=True, help_text="Contenido del archivo en Base64 o URL de Azure")
    NombreArchivo = models.CharField(max_length=255, null=True, blank=True,help_text="Nombre del archivo")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")
    
    class Meta:
        db_table = 'Consignaciones'
        default_permissions = ()
        
        
# ====================== AUDITORIA INTERNA ======================================
def consignaciones_post_save(sender, instance, created, *args, **kwargs):
        model_dict = model_to_dict(instance,
        foreign_keys=[
           
        ])
        model_dict.pop('model')
        model_dict['ConsignacionId'] = model_dict.pop('pk')
        ConsignacionesAuditoria.objects.create(**model_dict)

post_save.connect(consignaciones_post_save,sender=Consignaciones)
        
        
class ConsignacionesAuditoria(Auditoria):
    NumeroPlanilla = models.IntegerField(null=True, blank=True, help_text="ID de la planilla")
    TipoConsignacion = models.CharField(max_length=255, null=True, blank=True,help_text="Tipo de consignacion.")
    NumeroGuia = models.CharField(max_length=255, null=True, blank=True,help_text="Número de la guía asociada a la planilla")
    NumeroDocumento = models.CharField(max_length=255, null=True, blank=True,help_text="Número de documento o factura")
    NumeroConsignacion  = models.IntegerField(null=True, blank=True, help_text="Número de consignacion (Id auto-incremental)")
    NumeroConsignacionBanco  = models.CharField(max_length=255, null=True, blank=True, help_text="Número de consignacion banco")
    FechaRegistroCorta = models.CharField(max_length=100, null=True, blank=True, help_text="Fecha de registro yyyymmdd")
    FechaConsignacionCorta = models.CharField(max_length=100, null=True, blank=True, help_text="Fecha de consignacion yyyymmdd")
    FechaRegistroFull = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación yyyymmdd hh:mm:ss")
    FechaConsignacionFull = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de creación yyyymmdd hh:mm:ss")
    ValorConsignacion = models.DecimalField(max_digits=18, decimal_places=4, null=True, blank=True, help_text="Valor de la consignacion")
    RutaArchivoSoporte = models.TextField(null=True, blank=True, help_text="Contenido del archivo en Base64 o URL de Azure")
    NombreArchivo = models.CharField(max_length=255, null=True, blank=True,help_text="Nombre del archivo")
    Estado = models.BooleanField(default=True, help_text="Estado del atributo (activo/inactivo)")
    ConsignacionId = models.IntegerField(null=True, blank=True, help_text="ID de la auditoria de la consignacion")

    class Meta:
        db_table = 'ConsignacionessAuditoria'
        default_permissions = ()
        
        
class ErrorLogs(Auditoria):
    Consecutivo = models.IntegerField(null=True, blank=True, help_text="Hace refenrica al consecutivo.")
    Funcion = models.CharField(max_length=255, null=True, blank=True, help_text="Hace referencia alnombre la funcion")
    RequestData = models.JSONField(help_text="Hace referencia a la data enviada.", null=True)
    ResponseData = models.JSONField(help_text="Hace referencia a la data de respuesta.", null=True)
    ErrorTipo = models.CharField(max_length=255, null=True, blank=True)
    Mensaje = models.TextField(help_text="Hace referencia al mensjae de error", null=True, blank=True)
    Stacktrace = models.TextField()
    Fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ErrorLogs'
        default_permissions = ()
import json
from decimal import Decimal
from django.utils.timezone import now
from meicobaseapi.core.func.generals_gaw import GoAnyWhere
from meicobaseapi.enums.GoAnWhere.gaw_enum import GawEnums, CredencialesGaw
from meicobaseapi.models import( Documentos, DocumentosAuditoria, PlanillaDetalleFactura, 
                                PlanillaDetalles, PlanillaEncabezado)

class GestionRepository:
    
    
    def ws_planilla_detalle(self, request):
        """
            - Funcion que orquesta la conexion, paramtros 
            y repsuesta con Gaw para realizar el mapeo de campos 
        """
        try:

            payload = {
                "Pe_vcFecha": request.get('fecha'),
                "pe_vcBodega": request.get('bodega_id')
            }
            
            new_url = GoAnyWhere.request_with_basic_auth(GawEnums.GET_INFO_GUIAS.value, CredencialesGaw.USER_GAW.value, CredencialesGaw.PASSWORD_GAW.value, method="GET")
            if new_url:
                data = GoAnyWhere.request_with_basic_auth(str(new_url), CredencialesGaw.USER_GAW.value, CredencialesGaw.PASSWORD_GAW.value, method="POST", validate=True, data=payload)
                detalle = json.loads(data)       
                message_json = detalle["data"]["message"]
                
                parsed = json.loads(message_json)
                # Mapeo de estructuras
                facturas = parsed["PlanillaDetalleFacturas"]
   
                detalles = parsed["PlanillaDetalles"]
                documentos = parsed["Documentos"]
                
                if documentos not in (None, "", [], {}, 0):
                    self.procesar_documentos(documentos)
                    
                if detalles not in (None, "", [], {}, 0):
                    self.procesar_detalles(detalles)
                    
                if facturas not in (None, "", [], {}, 0):
                    self.procesar_detalles_facturas(facturas)
                    
            return []
        except Exception as e:
            raise e
        
        
    def procesar_documentos(self, json_data):
        """
        - Funcion que realiza un Create masivo a la tabla de documentos 
            segun se haga el consumo a GoAnyWhere
        """
        try:
            print("Esta en la funcion procesar_documentos *_*")
            print("======================================")            
            documentos_data = json_data.get("Documentos", [])
            
            documentos_objs = []
            auditoria_objs = []
            for item in documentos_data:
                documentos_objs.append(
                    Documentos(
                        PlanillaEncId=item.get("PlanillaEncId"),
                        IdGoAnyWhere=item.get("GoanywhereId"),
                        NumeroGuia=item.get("NumeroGuia"),
                        NumeroDocumento=item.get("NumeroDocumento"),
                        TipoDocumento=item.get("TipoDocumento"),
                        ValorDocumento=item.get("ValorDocumento"),
                        FechaDocumento=item.get("FechaDocumento"),
                        AplicaA=item.get("AplicaA"),
                        BodegaId=item.get("BodegaId"),
                        NombreBodega=item.get("NombreBodega"),
                        CodigoCliente=item.get("CodigoCliente"),
                        NombreCliente=item.get("NombreCliente"),
                        CondicionPago=item.get("CodigoCondicionPago"),
                        NombreCondicionPago=item.get("NombreCondicionPago"),
                        # Campos heredados de Auditoria
                        CreatedAt=now(),
                        UpdatedAt=now(),
                    )
                )
        
            # Bulk create
            Documentos.objects.bulk_create(documentos_objs, batch_size=500)
            print("Salio en la funcion procesar_documentos -_-")
            print("======================================")
            
            return len(documentos_objs)
        except Exception as e:
            raise e


    def procesar_detalles(self, json_data):
        """
        - Funcion que realiza un Create masivo a la tabla de documentos 
            segun se haga el consumo a GoAnyWhere
        """
        try:
            print("Esta en la funcion procesar_detalles *_*")
            print("======================================")  
            detalles = json_data.get("PlanillaDetalles", [])
               
            planilla_detalles_objs = []
            
            for item in detalles:
                planilla_detalles_objs.append(
                    PlanillaDetalles(
                        PlanillaEncId=item.get("PlanillaEncId"),
                        IdGoAnyWhere=item.get("GoanywhereId"),
                        NumeroGuia=item.get("NumeroGuia"),
                        FechaCreacionGuia=item.get("FechaCreacionGuia"),
                        FechaDespachoGuia=item.get("FechaDespachoGuia"),
                        TipoGuia=item.get("TipoGuia"),
                        BodegaId=item.get("BodegaId"),
                        TipoIdPropietarioTransportador=item.get("TipoIdPropietarioTransportador"),
                        IdPropietarioTransportador=item.get("IdPropietarioTransportador"),
                        NombrePropietarioTransportador=item.get("NombrePropietarioTransportador"),
                        Placa=item.get("Placa"),
                        TipoIdConductor=item.get("TipoIdConductor"),
                        ConductorId=item.get("ConductorId"),
                        NombreConductor=item.get("NombreConductor"),
                        EstadoGuia=item.get("EstadoGuia"),
                        CantidadFacturas=item.get("CantidadFacturas"),
                        FechaPromesa=item.get("FechaPromesa"),
                        FechaRetorno=item.get("FechaRetorno"),
                        ValorRecaudar=item.get("ValorRecaudar"),
                    )
                )

            PlanillaDetalles.objects.bulk_create(planilla_detalles_objs, batch_size=500)
            print("Salio en la funcion procesar_detalles -_-")
            print("======================================")
            return len(planilla_detalles_objs)
        except Exception as e:
            raise e


    def procesar_detalles_facturas(self, json_data):
        """
        - Funcion que realiza un Create masivo a la tabla de detalles facutras 
            segun se haga el consumo a GoAnyWhere
        """
        try:
            
            print("Esta en la funcion procesar_detalles_facturas *_*")
            print("======================================")  
            detalles = json_data.get("PlanillaDetalleFactura", [])
            
            planilla_factura_objs = []
    
            for item in detalles:
                planilla_factura_objs.append(
                    PlanillaDetalleFactura(
                        PlanillaEncId=item.get("PlanillaEncId"),
                        NumeroGuia=item.get("NumeroGuia"),
                        BodegaId=item.get("Bodega"),
                        FechaCreacionGuia=item.get("FechaCreacionGuia"),
                        FechaDespachoGuia=item.get("FechaDespacho"),
                        TipoGuia=item.get("TipoGuia"),
                        TipoIdPropietarioTransportador=item.get("TipoIdPropietarioTransportador"),
                        IdPropietarioTransportador=item.get("IdPropietarioTransportador"),
                        NombrePropietarioTransportador=item.get("NombrePropietarioTransportador"),
                        Placa=item.get("Placa"),
                        TipoIdConductor=item.get("TipoIdConductor"),
                        ConductorId=item.get("ConductorId"),
                        NombreConductor=item.get("NombreConductor"),
                        EstadoGuiaOriginal=item.get("EstadoGuiaOriginal"),
                        EstadoGuia=item.get("EstadoGuia"),
                        FechaPromesa=item.get("FechaPromesa"),
                        FechaRetorno=item.get("FechaRetorno"),
                        IdGoAnyWhere=item.get("GoanywhereId"),
                        NumeroDocumento=item.get("NumeroDocumento"),
                        TipoDocumento=item.get("TipoDocumento"),
                        CodigoCliente=item.get("CodigoCliente"),
                        RazonSocialCliente=item.get("RazonSocialCliente"),
                        ValorDevolucion=item.get("ValorDevolucion"),
                        ValorFactura=item.get("ValorFactura"),
                        DfrFactura=item.get("DfrFactura"),
                        NumerosNc=item.get("NumerosNc"),
                        ValorNc=item.get("ValorNc"),
                        DfrReal=item.get("DfrReal"),
                        ValorEsperadoRecaudar=item.get("ValorEsperadoRecaudar"),
                        ValorRecaudado=item.get("ValorRecaudado"),
                        Diferencia=Decimal(item.get("ValorEsperadoRecaudar")) - Decimal(item.get("ValorRecaudado")),
                        CodigoCondicionPago=item.get("CodigoCondicionPago"),
                        NombreCondicionPago=item.get("NombreCondicionPago"),
                    )
                )
    
            PlanillaDetalleFactura.objects.bulk_create(planilla_factura_objs, batch_size=500)

            print("Salio en la funcion procesar_detalles_facturas -_-")
            print("======================================")
            return len(planilla_factura_objs)
        except Exception as e:
            raise e 
        
        
    def get_all_planilla_encabezado(self):
        try:
            data = PlanillaEncabezado.objects.filter(estado=True).order_by('-id')
            return data
        except Exception as e:
            raise e
    

from decimal import Decimal
import json
from meicobaseapi.core.func.generals_gaw import GoAnyWhere
from meicobaseapi.enums.GoAnWhere.gaw_enum import GawEnums, CredencialesGaw
from meicobaseapi.models import( Documentos, PlanillaDetalleFactura, 
                                PlanillaDetalles, PlanillaEncabezado)

class GestionRepository:
    
    
    def ws_planilla_detalle(self, request):
        try:
            print("request: ", request)

            payload = {
                "Pe_vcFecha": request.get('fecha'),
                "pe_vcBodega": request.get('bodega_id'),
                #"pe_vcIdGaw": "1000"
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
        
            for item in documentos_data:
                documentos_objs.append(
                    Documentos(
                        planilla_enc_id=item.get("PlanillaEncId"),
                        id_go_any_where=item.get("GoanywhereId"),
                        numero_guia=item.get("NumeroGuia"),
                        numero_documento=item.get("NumeroDocumento"),
                        tipo_documento=item.get("TipoDocumento"),
                        valor_documento=item.get("ValorDocumento"),
                        fecha_documento=item.get("FechaDocumento"),
                        aplica_a=item.get("AplicaA"),
                        bodega_id=item.get("BodegaId"),
                        nombre_bodega=item.get("NombreBodega"),
                        codigo_cliente=item.get("CodigoCliente"),
                        nombre_cliente=item.get("NombreCliente"),
                        condicion_pago=item.get("CodigoCondicionPago"),
                        nombre_condicion_pago=item.get("NombreCondicionPago"),
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
            detalles = json_data.get("PlanillaDetalles", [])
            print("Esta en la funcion procesar_detalles *_*")
            print("======================================")  
               
            planilla_detalles_objs = []
            
            for item in detalles:
                planilla_detalles_objs.append(
                    PlanillaDetalles(
                        planilla_enc_id=item.get("PlanillaEncId"),
                        id_go_any_where=item.get("GoanywhereId"),
                        numero_guia=item.get("NumeroGuia"),
                        fecha_creacion_guia=item.get("FechaCreacionGuia"),
                        fecha_despacho_guia=item.get("FechaDespachoGuia"),
                        tipo_guia=item.get("TipoGuia"),
                        bodega_id=item.get("BodegaId"),
                        tipo_id_propietario_transportador=item.get("TipoIdPropietarioTransportador"),
                        id_propietario_transportador=item.get("IdPropietarioTransportador"),
                        nombre_propietario_transportador=item.get("NombrePropietarioTransportador"),
                        placa=item.get("Placa"),
                        tipo_id_conductor=item.get("TipoIdConductor"),
                        conductor_id=item.get("ConductorId"),
                        nombre_conductor=item.get("NombreConductor"),
                        estado_guia=item.get("EstadoGuia"),
                        cantidad_facturas=item.get("CantidadFacturas"),
                        fecha_promesa=item.get("FechaPromesa"),
                        fecha_retorno=item.get("FechaRetorno"),
                        valor_recaudar=item.get("ValorRecaudar"),
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
            
            detalles = json_data.get("PlanillaDetalleFactura", [])
            print("Esta en la funcion procesar_detalles_facturas *_*")
            print("======================================")  
            
            planilla_factura_objs = []
    
            for item in detalles:
                planilla_factura_objs.append(
                    PlanillaDetalleFactura(
                        planilla_enc_id=item.get("PlanillaEncId"),
                        numero_guia=item.get("NumeroGuia"),
                        bodega_id=item.get("Bodega"),
                        fecha_creacion_guia=item.get("FechaCreacionGuia"),
                        fecha_despacho_guia=item.get("FechaDespacho"),
                        tipo_guia=item.get("TipoGuia"),
                        tipo_id_propietario_transportador=item.get("TipoIdPropietarioTransportador"),
                        id_propietario_transportador=item.get("IdPropietarioTransportador"),
                        nombre_propietario_transportador=item.get("NombrePropietarioTransportador"),
                        placa=item.get("Placa"),
                        tipo_id_conductor=item.get("TipoIdConductor"),
                        conductor_id=item.get("ConductorId"),
                        nombre_conductor=item.get("NombreConductor"),
                        estado_guia_original=item.get("EstadoGuiaOriginal"),
                        estado_guia=item.get("EstadoGuia"),
                        fecha_promesa=item.get("FechaPromesa"),
                        fecha_retorno=item.get("FechaRetorno"),
                        id_go_any_where=item.get("GoanywhereId"),
                        numero_documento=item.get("NumeroDocumento"),
                        tipo_documento=item.get("TipoDocumento"),
                        codigo_cliente=item.get("CodigoCliente"),
                        razon_social_cliente=item.get("RazonSocialCliente"),
                        valor_devolucion=item.get("ValorDevolucion"),
                        valor_factura=item.get("ValorFactura"),
                        dfr_factura=item.get("DfrFactura"),
                        numeros_nc=item.get("NumerosNc"),
                        valor_nc=item.get("ValorNc"),
                        dfr_real=item.get("DfrReal"),
                        valor_esperado_recaudar=item.get("ValorEsperadoRecaudar"),
                        valor_recaudado=item.get("ValorRecaudado"),
                        diferencia=Decimal(item.get("ValorEsperadoRecaudar")) - Decimal(item.get("ValorRecaudado"))
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
    

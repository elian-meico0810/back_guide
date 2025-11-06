from datetime import datetime
from decimal import Decimal
import json
from meicobaseapi.core.func.generals_gaw import GoAnyWhere
from meicobaseapi.enums.GoAnWhere.gaw_enum import GawEnums, CredencialesGaw
from meicobaseapi.models import PlanillaDetalles, PlanillaEncabezado, Usuarios
from django.db import connection
from django.db import transaction
from django.utils import timezone

class GestionRepository:
    
    
    def ws_planilla_detalle(self):
        try:
            payload = {
                "Fecha": "2024-08-31",
                "Bodega": "1"
            }
            new_url = GoAnyWhere.request_with_basic_auth(GawEnums.GET_INFO_GUIAS.value, CredencialesGaw.USER_GAW.value, CredencialesGaw.PASSWORD_GAW.value, method="GET")
            #if new_url:
            #    print("new_url: ",new_url)
            #    data = GoAnyWhere.request_with_basic_auth(str(new_url), CredencialesGaw.USER_GAW.value, CredencialesGaw.PASSWORD_GAW.value, method="POST", validate=True,data=payload)
            #    detalle =  json.loads(data)
            #    facturas_detalladas = json.loads(detalle["data"]["message"]).get("FacturasDetalladas", [])
#
            #    #  Iterar sobre cada registro y crear objetos en DB
            #    for factura in facturas_detalladas:
            #        print("factura: ",factura)
            #        id_go_any_where = factura.get("idGoAnyWhere", None)
            #        numero_guia = factura.get("NumeroGuia", None)
            #        origen = factura.get("Origen", None)
            #        transportador = factura.get("Transportador", None)
            #        codigo_cliente = factura.get("CodigoCliente", None)
            #        nombre_cliente = factura.get("NombreCliente", None)
            #        ciudad = factura.get("Ciudad", None)
            #        numero_factura = factura.get("NumeroFactura", None)
            #        cantidad_notas_credito = factura.get("CantidadNotasCredito", None)
            #        fecha_factura = factura.get("FechaFactura", None)
            #        vendedor = factura.get("Vendedor", None)
            #        valor_original = Decimal(factura.get("ValorOriginal", 0))
            #        dscto_financiero = Decimal(factura.get("DsctoFinanciero", 0))
            #        nuevo_dscto_financiero = Decimal(factura.get("NuevoDsctoFinanciero", 0))
            #        cantidad_nota_credito = factura.get("CantidadNotaCredito", None)
            #        valor_nota_credito = factura.get("ValorNotaCredito", None)
            #        lista_notas_credito = factura.get("ListaNotasCredito", None)
            #        total_notas_credito = Decimal(factura.get("TotalNotasCredito", 0))
            #        tiene_nota_credito = factura.get("TieneNotaCredito", None)
            #        tipo_forma_pago = factura.get("TipoFormaPago", None)
            #        bodega = factura.get("Bodega", None)
            #        valor_consignar = Decimal(factura.get("ValorConsignar", 0))
            #        reporte_brinks = factura.get("ReporteBrinks", 0)
            #        diferencia_valor = Decimal(factura.get("DiferenciaValor", 0))
            #        fecha_despacho_completa = factura.get("FechaDespachoCompleta", None)
            #        observaciones = factura.get("Observaciones", None)
            #        cargue = factura.get("Cargue", None)                    
            #        print("response: ",cargue)
            #        print("reporte_brinks: ",reporte_brinks)
         #
            #        planilla_detalle = PlanillaDetalles.objects.create(
            #            planilla_enc_id=None,  # luego se actualizará con el autoincremental
            #            id_go_any_where=id_go_any_where,
            #            numero_guia=numero_guia,
            #            fecha_creacion_guia="No está",
            #            fecha_despacho_guia=fecha_despacho_completa,
            #            tipo_guia=origen,
            #            bodega_id=bodega,
            #            tipo_id_propietario_transportador="C.C",
            #            id_propietario_transportador="No está",
            #            nombre_propietario_transportador=transportador,
            #            placa="No está",
            #            tipo_id_conductor="No está",
            #            conductor_id="No está",
            #            estado_guia_original="No está",
            #            estado_guia="No está",
            #            cantidad_facturas=None,    
            #            fecha_promesa="No está",
            #            fecha_retorno="No está",
            #            valor_recaudar=None,        
            #            estado=True
            #        )
#
            #        planilla_detalle.planilla_enc_id = planilla_detalle.id
            #        planilla_detalle.save()
                    
            data = PlanillaDetalles.objects.filter(estado=True)
            return data
        except Exception as e:
            raise e
        
    def get_all_planilla_encabezado(self):
        try:
            data = PlanillaEncabezado.objects.filter(estado=True)
            return data
        except Exception as e:
            raise e
    

from django.db.models import Sum, Max, Q
from django.db.models.functions import Lower
from meicobaseapi.models import PlanillaDetalles, PlanillaDetalleFactura

class PlanillaDetallesRepository:
    
    def get_all(self):
        try:
            data = PlanillaDetalles.objects.filter(estado=True).order_by('-id')
            return data
        except Exception as e:
            raise e
    
  
    def get_details_guide(self, search=None):
        try:
            data = PlanillaDetalles.objects.filter(estado=True)

            # Solo aplicamos filtro si viene search
            if search:
                search_words = search.strip().split()
                for word in search_words:
                    data = data.filter(
                        Q(nombre_propietario_transportador__icontains=word) |
                        Q(numero_guia__icontains=word)
                    )
    
            # Valores que queremos devolver
            data = data.values(
                'planilla_enc_id',
                'id_go_any_where',
                'numero_guia',
                'fecha_creacion_guia',
                'estado_guia',
                'valor_recaudar',
                'nombre_propietario_transportador'
            ).distinct()

            resultado = []

            for p in data:
                # Facturas relacionadas activas con misma guía y planilla
                facturas = PlanillaDetalleFactura.objects.filter(
                    planilla_enc_id=p['planilla_enc_id'],
                    id_go_any_where=p['id_go_any_where'],
                    numero_guia=p['numero_guia'],
                    estado=True
                )

                cantidad_facturas = facturas.count()
                fecha_retorno_max = facturas.aggregate(
                    fecha_retorno_max=Max('created_at')
                )['fecha_retorno_max']

                resultado.append({
                    'planilla_enc_id': p['planilla_enc_id'],
                    'id_go_any_where': p['id_go_any_where'],
                    'numero_guia': p['numero_guia'],
                    'fecha_creacion_guia': p['fecha_creacion_guia'],
                    'estado_guia': p['estado_guia'],
                    'valor_recaudar': float(p['valor_recaudar'] or 0),
                    'transportador': p['nombre_propietario_transportador'],
                    'cantidad_facturas': cantidad_facturas,
                    'mayor_fecha_retorno': fecha_retorno_max
                })
            return resultado
        except Exception as e:
            raise e


    def get_totales_completos(self, search=None):
        try:
            guias = PlanillaDetalles.objects.filter(estado=True)

            guias = guias.annotate(estado_lower=Lower('estado_guia')).filter(
                estado_lower__in=['confirmada', 'despachada']
            )

            if search:
                search_words = search.strip().split()
                for word in search_words:
                    guias = guias.filter(
                        Q(nombre_propietario_transportador__icontains=word) |
                        Q(numero_guia__icontains=word)
                    )

            guias = guias.values(
                'planilla_enc_id',
                'id_go_any_where',
                'numero_guia',
                'estado_lower'
            ).distinct()

            total_confirmada = 0
            total_despachada = 0
            total_valor_esperado_recaudar = 0
            total_valor_recaudado = 0   

            # Sumamos por cada guía
            for g in guias:
                estado = g['estado_lower']
                facturas = PlanillaDetalleFactura.objects.filter(
                    estado=True,
                    planilla_enc_id=g['planilla_enc_id'],
                    id_go_any_where=g['id_go_any_where'],
                    numero_guia=g['numero_guia']
                )   

                agregados = facturas.aggregate(
                    total_esperado=Sum('valor_esperado_recaudar'),
                    total_recaudado=Sum('valor_recaudado')
                )   

                if estado == 'confirmada':
                    total_confirmada += 1
                elif estado == 'despachada':
                    total_despachada += 1   

                total_valor_esperado_recaudar += float(agregados['total_esperado'] or 0)
                total_valor_recaudado += float(agregados['total_recaudado'] or 0)   

            return {
                'total_confirmada': total_confirmada,
                'total_despachada': total_despachada,
                'total_valor_esperado_recaudar': total_valor_esperado_recaudar,
                'total_valor_recaudado': total_valor_recaudado
            }   

        except Exception as e:
            raise e 

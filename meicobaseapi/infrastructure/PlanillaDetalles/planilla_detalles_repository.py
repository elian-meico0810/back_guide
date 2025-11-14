from django.db.models import Sum, Max, Q, F
from django.db.models.functions import Lower
from meicobaseapi.models import PlanillaDetalles, PlanillaDetalleFactura

class PlanillaDetallesRepository:
    
    def get_all(self):
        try:
            data = PlanillaDetalles.objects.filter(Estado=True).order_by('-id')
            return data
        except Exception as e:
            raise e
    
  
    def get_details_guide(self, search, estado_guia, transportador, bodega_id):
        try:
            data = PlanillaDetalles.objects.filter(Estado=True)

            # Solo aplicamos filtro si viene search
            if search:
                search_words = search.strip().split()
                for word in search_words:
                    data = data.filter(
                        Q(NombrePropietarioTransportador__icontains=word) |
                        Q(NumeroGuia__icontains=word)
                    )
                    
            if estado_guia:
                data = data.filter(EstadoGuia=estado_guia) 
                
            if bodega_id:
                data = data.filter(BodegaId=bodega_id) 

            if transportador:
                data = data.filter(NombrePropietarioTransportador=transportador)   
                                  
            # Valores que queremos devolver
            data = data.values(
                'PlanillaEncId',
                'IdGoAnyWhere',
                'NumeroGuia',
                'FechaCreacionGuia',
                'EstadoGuia',
                'ValorRecaudar',
                'NombrePropietarioTransportador'
            ).distinct()

            resultado = []

            for p in data:
                # Facturas relacionadas activas con misma guía y planilla
                facturas = PlanillaDetalleFactura.objects.filter(
                    PlanillaEncId=p['PlanillaEncId'],
                    IdGoAnyWhere=p['IdGoAnyWhere'],
                    NumeroGuia=p['NumeroGuia'],
                    Estado=True
                )

                cantidad_facturas = facturas.count()
                fecha_retorno_max = facturas.aggregate(
                    fecha_retorno_max=Max('CreatedAt')
                )['fecha_retorno_max']

                resultado.append({
                    'PlanillaEncId': p['PlanillaEncId'],
                    'IdGoAnyWhere': p['IdGoAnyWhere'],
                    'NumeroGuia': p['NumeroGuia'],
                    'FechaCreacionGuia': p['FechaCreacionGuia'],
                    'EstadoGuia': p['EstadoGuia'],
                    'ValorRecaudar': float(p['ValorRecaudar'] or 0),
                    'Transportador': p['NombrePropietarioTransportador'],
                    'CantidadFacturas': cantidad_facturas,
                    'MayoFechaRetorno': fecha_retorno_max
                })
            return resultado
        except Exception as e:
            raise e


    def get_totales_completos(self, search, bodega_id):
        try:
            guias = PlanillaDetalles.objects.filter(Estado=True)

            guias = guias.annotate(Estado_lower=Lower('EstadoGuia')).filter(
                Estado_lower__in=['confirmada', 'despachada']
            )

            if search:
                search_words = search.strip().split()
                for word in search_words:
                    guias = guias.filter(
                        Q(NombrePropietarioTransportador__icontains=word) |
                        Q(NumeroGuia__icontains=word)
                    )
                    
            if bodega_id:
                guias = guias.filter(BodegaId=bodega_id) 
                
            guias = guias.values(
                'PlanillaEncId',
                'IdGoAnyWhere',
                'NumeroGuia',
                'Estado_lower'
            ).distinct()

            total_confirmada = 0
            total_despachada = 0
            total_valor_esperado_recaudar = 0
            total_valor_recaudado = 0   

            # Sumamos por cada guía
            for g in guias:
                estado = g['Estado_lower']
                facturas = PlanillaDetalleFactura.objects.filter(
                    Estado=True,
                    PlanillaEncId=g['PlanillaEncId'],
                    IdGoAnyWhere=g['IdGoAnyWhere'],
                    NumeroGuia=g['NumeroGuia']
                )   

                agregados = facturas.aggregate(
                    total_esperado=Sum('ValorEsperadoRecaudar'),
                    total_recaudado=Sum('ValorRecaudado')
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
        
        
    def get_parametros_filtro(self, bodega_id):
        try:
            data = PlanillaDetalles.objects.filter(Estado=True)

            if bodega_id:
                data = data.filter(BodegaId=bodega_id)

            # Creamos alias con annotate() usando F() y luego sacamos los valores
            data = data.annotate(
                EstadoRename=F('EstadoGuia'),
                Transportador=F('NombrePropietarioTransportador')
            ).values(
                'EstadoGuia',
                'Transportador'
            ).distinct()

            return data
        except Exception as e:
            raise e


    def get_numero_guia(self, search, estado_guia, transportador, bodega_id, numero_guia):
        try:
            data = PlanillaDetalles.objects.filter(Estado=True)

            # Solo aplicamos filtro si viene search
            if search:
                search_words = search.strip().split()
                for word in search_words:
                    data = data.filter(
                        Q(NombrePropietarioTransportador__icontains=word) |
                        Q(NumeroGuia__icontains=word)
                    )
                    
            if estado_guia:
                data = data.filter(EstadoGuia=estado_guia) 
                
            if bodega_id:
                data = data.filter(Bodega_id=bodega_id) 

            if transportador:
                data = data.filter(NombrePropietarioTransportador=transportador)   
            
            if numero_guia:
               data = data.filter(NumeroGuia=numero_guia)   
                    
            # Valores que queremos devolver
            data = data.values(
                'PlanillaEncId',
                'IdGoAnyWhere',
                'NumeroGuia',
                'FechaCreacionGuia',
                'EstadoGuia',
                'ValorRecaudar',
                'NombrePropietarioTransportador'
            ).distinct()

            resultado = []

            for p in data:
                # Facturas relacionadas activas con misma guía y planilla
                facturas = PlanillaDetalleFactura.objects.filter(
                    PlanillaEncId=p['PlanillaEncId'],
                    IdGoAnyWhere=p['IdGoAnyWhere'],
                    NumeroGuia=p['NumeroGuia'],
                    Estado=True
                )

                cantidad_facturas = facturas.count()
                fecha_retorno_max = facturas.aggregate(
                    fecha_retorno_max=Max('CreatedAt')
                )['fecha_retorno_max']

                resultado.append({
                    'PlanillaEncId': p['PlanillaEncId'],
                    'IdGoAnyWhere': p['IdGoAnyWhere'],
                    'NumeroGuia': p['NumeroGuia'],
                    'FechaCreacionGuia': p['FechaCreacionGuia'],
                    'EstadoGuia': p['EstadoGuia'],
                    'ValorRecaudar': float(p['ValorRecaudar'] or 0),
                    'Transportador': p['NombrePropietarioTransportador'],
                    'CantidadFacturas': cantidad_facturas,
                    'MayorFechaRetorno': fecha_retorno_max
                })
            return resultado
        except Exception as e:
            raise e
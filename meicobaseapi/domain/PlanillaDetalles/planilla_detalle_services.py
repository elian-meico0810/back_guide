from meicobaseapi.infrastructure.PlanillaDetalles.planilla_detalles_repository import PlanillaDetallesRepository


class PlanillaDetallesService:

    def __init__(self):
        self.repo = PlanillaDetallesRepository()


    def get_all_planilla_detalles(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e

       
    def get_all_detalle_guia(self, search, estado_guia, transportador, bodega_id):
        try:
            return self.repo.get_details_guide(search, estado_guia, transportador, bodega_id)
        except Exception as e:
            raise e
        
        
    def get_totals_guide(self, search, bodega_id):
        try:
            return self.repo.get_totales_completos(search, bodega_id)
        except Exception as e:
            raise e
        
    def get_filter(self, bodega_id):
        try:
            return self.repo.get_parametros_filtro(bodega_id)
        except Exception as e:
            raise e
        
    def get_numero_guia_ws(self, search, estado_guia, transportador, bodega_id, numero_guia):
        try:
            return self.repo.get_numero_guia(search, estado_guia, transportador, bodega_id, numero_guia)
        except Exception as e:
            raise e
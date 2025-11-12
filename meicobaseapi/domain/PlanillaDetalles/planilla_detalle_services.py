from meicobaseapi.infrastructure.PlanillaDetalles.planilla_detalles_repository import PlanillaDetallesRepository


class PlanillaDetallesService:

    def __init__(self):
        self.repo = PlanillaDetallesRepository()


    def get_all_planilla_detalles(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e

       
    def get_all_detalle_guia(self, search=None):
        try:
            return self.repo.get_details_guide(search)
        except Exception as e:
            raise e
        
        
    def get_totals_guide(self,search=None):
        try:
            return self.repo.get_totales_completos(search)
        except Exception as e:
            raise e
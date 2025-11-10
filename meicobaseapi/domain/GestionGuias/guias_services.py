
from meicobaseapi.infrastructure.PlanillaEncabezado.planilla_encabezado_repository import PlanillaEncabezadoRepository


class PlanillaEncabezadoService:

    def __init__(self):
        self.repo = PlanillaEncabezadoRepository()


    def get_all_planilla_encabezado(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e
        
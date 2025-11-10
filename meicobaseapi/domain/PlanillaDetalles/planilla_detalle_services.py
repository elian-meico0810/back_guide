from meicobaseapi.infrastructure.GestionGuias.gestion_repository import GestionRepository

class GuiasService:

    def __init__(self):
        self.repo = GestionRepository()


    def get_all_planilla_detalles(self):
        try:
            return self.repo.ws_planilla_detalle()
        except Exception as e:
            raise e
        
        
    def get_all_planilla_encabezado(self):
        try:
            return self.repo.get_all_planilla_encabezado()
        except Exception as e:
            raise e
  
from meicobaseapi.infrastructure.GestionGuias.gestion_repository import GestionRepository


class GestionRepositoryService:

    def __init__(self):
        self.repo = GestionRepository()


    def ws_db_erp(self, request):
        try:
            return self.repo.ws_planilla_detalle(request)
        except Exception as e:
            raise e
        
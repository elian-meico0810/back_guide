from meicobaseapi.infrastructure.Consignaciones.consignaciones_repository import ConsignacionesRepository


class ConsignacionesService:

    def __init__(self):
        self.repo = ConsignacionesRepository()


    def get_all_consignaciones(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e
        
        
    def create_consignaciones(self, data):
        try:
            return self.repo.upload_file(data)
        except Exception as e:
            raise e
        
        
    def get_group_parametros(self):
        try:
            return self.repo.group_parameer()
        except Exception as e:
            raise e
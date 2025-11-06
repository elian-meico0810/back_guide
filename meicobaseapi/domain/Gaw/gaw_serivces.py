from meicobaseapi.infrastructure.Gaw.gaw_repository import GawRepository

class GawService:
    def __init__(self):
        self.repo = GawRepository()

    def ws_info_guias(self):
        try:
            return self.repo.ws_ingo_guias()
        except Exception as e:
            raise e
    
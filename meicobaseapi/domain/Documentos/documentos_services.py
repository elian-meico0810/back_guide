from meicobaseapi.infrastructure.Documentos.documentos_repository import DocumentosRepository


class DocumentosService:

    def __init__(self):
        self.repo = DocumentosRepository()


    def get_all_documentos(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e
        
        
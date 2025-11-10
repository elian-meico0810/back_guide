from meicobaseapi.models import Documentos
from django.db import connection
from django.db import transaction
from django.utils import timezone

class DocumentosRepository:
    
    def get_all(self):
        try:
            data = Documentos.objects.filter(estado=True)
            return data
        except Exception as e:
            raise e
    
  

from meicobaseapi.models import Consignaciones
from django.db import connection
from django.db import transaction
from django.utils import timezone

class ConsignacionesRepository:
    
    def get_all(self):
        try:
            data = Consignaciones.objects.filter(estado=True)
            return data
        except Exception as e:
            raise e
    
    
    def upload_file(self , data):
        try:
            return Consignaciones.objects.create(**data)
        except Exception as e:
            raise e
  

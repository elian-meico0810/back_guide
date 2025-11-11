from meicobaseapi.models import PlanillaDetalles
from django.db import connection
from django.db import transaction
from django.utils import timezone

class PlanillaDetallesRepository:
    
    def get_all(self):
        try:
            data = PlanillaDetalles.objects.filter(estado=True).order_by('-id')
            return data
        except Exception as e:
            raise e
    
  

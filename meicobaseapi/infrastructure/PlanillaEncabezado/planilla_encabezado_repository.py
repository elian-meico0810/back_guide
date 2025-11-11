from meicobaseapi.models import PlanillaEncabezado
from django.db import connection
from django.db import transaction
from django.utils import timezone

class PlanillaEncabezadoRepository:
    
    def get_all(self):
        try:
            data = PlanillaEncabezado.objects.filter(estado=True).order_by('-id')
            return data
        except Exception as e:
            raise e
    
  

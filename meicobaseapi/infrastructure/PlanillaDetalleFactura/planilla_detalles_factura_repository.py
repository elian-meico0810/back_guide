from meicobaseapi.models import PlanillaDetalleFactura
from django.db import connection
from django.db import transaction
from django.utils import timezone

class PlanillaDetalleFacturaRepository:
    
    def get_all(self):
        try:
            data = PlanillaDetalleFactura.objects.filter(estado=True)
            return data
        except Exception as e:
            raise e
    
  

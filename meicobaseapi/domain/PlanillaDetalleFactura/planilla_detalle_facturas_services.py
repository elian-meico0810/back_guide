from meicobaseapi.infrastructure.PlanillaDetalleFactura.planilla_detalles_factura_repository import PlanillaDetalleFacturaRepository


class  PlanillaDetallesService:

    def __init__(self):
        self.repo = PlanillaDetalleFacturaRepository()


    def get_all_planilla_detalle_facturas(self):
        try:
            return self.repo.get_all()
        except Exception as e:
            raise e
        
        
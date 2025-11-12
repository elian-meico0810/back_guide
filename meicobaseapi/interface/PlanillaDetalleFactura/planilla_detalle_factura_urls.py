from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meicobaseapi.interface.PlanillaDetalleFactura.planilla_detalle_factura_views import PlanillaDetalleFacturaViewSet


router = DefaultRouter()
router.register(r'planilla-detalle-facturas', PlanillaDetalleFacturaViewSet, basename='planilla-detalle-facturas')

urlpatterns = [
    path('', include(router.urls)),
]

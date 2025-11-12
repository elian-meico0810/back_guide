from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meicobaseapi.interface.PlanillaDetalles.planilla_detalle_views import PlanillaDetallesViewSet

router = DefaultRouter()
router.register(r'planilla-detalle', PlanillaDetallesViewSet, basename='planilla-detalle')

urlpatterns = [
    path('', include(router.urls)),
]

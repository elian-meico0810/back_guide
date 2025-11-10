from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meicobaseapi.interface.Consignaciones.consignaciones_views import ConsignacionesViewSet

router = DefaultRouter()
router.register(r'consignaciones', ConsignacionesViewSet, basename='consignaciones')

urlpatterns = [
    path('', include(router.urls)),
]

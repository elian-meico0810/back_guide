from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meicobaseapi.interface.GestionGuias.gestion_views import GestionViewSet

router = DefaultRouter()
router.register(r'gestionGuias', GestionViewSet, basename='gestionGuias')

urlpatterns = [
    path('', include(router.urls)),
]

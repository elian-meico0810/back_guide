from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meicobaseapi.interface.Usuarios.usuarios_views import UsuariosViewSet

router = DefaultRouter()
router.register(r'users', UsuariosViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]

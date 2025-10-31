from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meicobaseapi.interface.Roles.roles_views import RolesViewSet

router = DefaultRouter()
router.register(r'groups', RolesViewSet, basename='groups')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from meicobaseapi.interface.Gaw.gaw_views import GawViewSet

router = DefaultRouter()
router.register(r'ws-gaw', GawViewSet, basename='ws-gaw')

urlpatterns = [
    path('', include(router.urls)),
]

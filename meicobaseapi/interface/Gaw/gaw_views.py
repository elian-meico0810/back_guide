from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.decorators import permission_classes
from meicobaseapi.core.helpers.utils import formatErrors
from meicobaseapi.core.pagination.custom_pagination import PaginationHandlerMixin, ResultsSetPagination
from meicobaseapi.core.APIResponse import APIResponse
from meicobaseapi.core.authentication import AllowAnonymous
from meicobaseapi.core.jwt_auth import JWTAuthentication
from meicobaseapi.infrastructure.Gaw.gaw_repository import GawRepository
from meicobaseapi.interface.Gaw.gaw_serializers import GawListSerializer


class GawViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    service = GawRepository()
    # Definimos el serializador primcipal
    serializer_class = GawListSerializer
    # Definimos el serializador para listas primicipal
    list_serializer_class = GawListSerializer
    # Aplicamos la paginacion
    pagination_class = ResultsSetPagination


    @swagger_auto_schema(tags=["gaw"])
    @action(detail=False, methods=["GET"], url_path="obtener", name="Obtener infomacion")
    @permission_classes([AllowAnonymous])
    def obtener_usuarios(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            gaw = self.service.ws_ingo_guias()

            paginator = self.pagination_class()

            page = request.query_params.get("page", None)

            if page is not None:
                # Aplica paginación
                paginated_users = paginator.paginate_queryset(gaw, request)
                serializer = self.list_serializer_class(paginated_users, many=True)
                data = paginator.get_paginated_response(serializer.data).data
            else:
                # Devuelve todos los resultados sin paginar
                serializer = self.list_serializer_class(gaw, many=True)
                data = serializer.data

            return APIResponse.successful(
                message="Operación exitosa",
                data=data
            )

        except Exception as e:
            return APIResponse.failed(e)

   
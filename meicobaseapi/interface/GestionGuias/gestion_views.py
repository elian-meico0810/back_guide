from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.decorators import permission_classes
from meicobaseapi.core.helpers.utils import formatErrors
from meicobaseapi.core.pagination.custom_pagination import PaginationHandlerMixin, ResultsSetPagination
from meicobaseapi.domain.GestionGuias.guias_services import GuiasService
from meicobaseapi.interface.GestionGuias.gestion_serializers import PlanillaDetallesListSerializer, PlanillaListSerializer
from meicobaseapi.core.APIResponse import APIResponse
from meicobaseapi.core.authentication import AllowAnonymous


class GestionViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    service = GuiasService()
    # Definimos el serializador primcipal
    serializer_class = None
    # Definimos el serializador para listas primicipal
    list_serializer_class = PlanillaDetallesListSerializer
    # Aplicamos la paginacion
    pagination_class = ResultsSetPagination


    @swagger_auto_schema(tags=["gestionGuias"])
    @action(detail=False, methods=["GET"], url_path="obtener-planilla-detalles", name="Obtener detalle de planillas")
    @permission_classes([AllowAnonymous])
    def obtener_planilla_detalle(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            users = self.service.get_all_planilla_detalles()

            paginator = self.pagination_class()

            page = request.query_params.get("page", None)

            if page is not None:
                # Aplica paginación
                paginated_users = paginator.paginate_queryset(users, request)
                serializer = self.list_serializer_class(paginated_users, many=True)
                data = paginator.get_paginated_response(serializer.data).data
            else:
                # Devuelve todos los resultados sin paginar
                serializer = self.list_serializer_class(users, many=True)
                data = serializer.data

            return APIResponse.successful(
                message="Operación exitosa",
                data=data
            )

        except Exception as e:
            return APIResponse.failed(e)
        
        
        
    @swagger_auto_schema(tags=["gestionGuias"])
    @action(detail=False, methods=["GET"], url_path="obtener-encabezado-planillas", name="Obtener encabezado de planillas")
    @permission_classes([AllowAnonymous])
    def obtener_encabezado_planilla(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            users = self.service.get_all_planilla_encabezado()

            paginator = self.pagination_class()

            page = request.query_params.get("page", None)

            if page is not None:
                # Aplica paginación
                paginated_users = paginator.paginate_queryset(users, request)
                serializer = PlanillaListSerializer(paginated_users, many=True)
                data = paginator.get_paginated_response(serializer.data).data
            else:
                # Devuelve todos los resultados sin paginar
                serializer = PlanillaListSerializer(users, many=True)
                data = serializer.data

            return APIResponse.successful(
                message="Operación exitosa",
                data=data
            )

        except Exception as e:
            return APIResponse.failed(e)


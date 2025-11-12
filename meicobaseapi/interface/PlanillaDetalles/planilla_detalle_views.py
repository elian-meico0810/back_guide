from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from meicobaseapi.core.jwt_auth import JWTAuthentication
from meicobaseapi.core.pagination.custom_pagination import PaginationHandlerMixin, ResultsSetPagination
from meicobaseapi.core.APIResponse import APIResponse
from meicobaseapi.core.authentication import AllowAnonymous
from meicobaseapi.domain.PlanillaDetalles.planilla_detalle_services import PlanillaDetallesService
from rest_framework.decorators import action, permission_classes
from meicobaseapi.interface.PlanillaDetalles.planilla_detalle_serializers import PlanillaDetallesListSerializer, PlanillaDetallesSerializer
 
class PlanillaDetallesViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    service =  PlanillaDetallesService()
    # Definimos el serializador primcipal
    serializer_class = PlanillaDetallesSerializer
    # Definimos el serializador para listas primicipal
    list_serializer_class = PlanillaDetallesListSerializer
    # Aplicamos la paginacion
    pagination_class = ResultsSetPagination
    # Validamos la autentiacion
    authentication_classes= [JWTAuthentication]
 

    @swagger_auto_schema(tags=["PlanillaDetalle"])
    @action(detail=False, methods=["GET"], url_path="obtener-planilla-detalles", name="Obtener planilla detalle")
    @permission_classes([AllowAnonymous])
    def obtener_planilla_detalle(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            data = self.service.get_all_planilla_detalles()

            paginator = self.pagination_class()

            page = request.query_params.get("page", None)
            search = request.query_params.get("search", None)

            #============================================================
            if page is not None:
                # Aplica paginación
                paginated_users = paginator.paginate_queryset(data, request)
                serializer = self.list_serializer_class(paginated_users, many=True)
                data = paginator.get_paginated_response(serializer.data).data
            else:
                # Devuelve todos los resultados sin paginar
                serializer = self.list_serializer_class(data, many=True)
                data = serializer.data

            return APIResponse.successful(
                message="Operación exitosa",
                data=data
            )
        except Exception as e:
            return APIResponse.failed(e)
        
        
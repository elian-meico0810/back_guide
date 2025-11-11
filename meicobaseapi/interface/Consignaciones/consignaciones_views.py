from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.decorators import permission_classes
from meicobaseapi.core.helpers.utils import formatErrors
from meicobaseapi.core.pagination.custom_pagination import PaginationHandlerMixin, ResultsSetPagination
from meicobaseapi.domain.Consignaciones.consignaciones_services import ConsignacionesService
from meicobaseapi.core.APIResponse import APIResponse
from meicobaseapi.core.authentication import AllowAnonymous
from meicobaseapi.interface.Consignaciones.consignaciones_serializers import ConsignacionesListSerializer, ConsignacionesSerializer


class ConsignacionesViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    service =  ConsignacionesService()
    # Definimos el serializador primcipal
    serializer_class = ConsignacionesSerializer
    # Definimos el serializador para listas primicipal
    list_serializer_class = ConsignacionesListSerializer
    # Aplicamos la paginacion
    pagination_class = ResultsSetPagination


    @swagger_auto_schema(tags=["consignaciones"])
    @action(detail=False, methods=["GET"], url_path="obtener-consignaciones", name="Obtener consignaciones")
    @permission_classes([AllowAnonymous])
    def obtener_planilla_detalle(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            data = self.service.get_all_consignaciones()

            paginator = self.pagination_class()

            page = request.query_params.get("page", None)
            search = request.query_params.get("search", None)

            if search:
                data = data.filter(Q(fecha_consignacion_corta__icontains=search) |
                                Q(tipo_consignacion__icontains=search) |  
                                Q(valor_consignacion__icontains=search) | 
                                Q(nombre_archivo__icontains=search) )
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
        
        
    @swagger_auto_schema(tags=["consignaciones"])
    @action(detail=False, methods=["POST"], url_path="crear", name="Crear consignacion")
    @permission_classes([AllowAnonymous])
    def crear_consignaciones(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                self.service.create_consignaciones(request.data)
            else:
                return APIResponse.failed(error=formatErrors(serializer.errors))
             
            return APIResponse.successful(message="Operación exitosa", data=[])
        except Exception as e:
            return APIResponse.failed(e)
        
        
    @swagger_auto_schema(tags=["consignaciones"])
    @action(detail=False, methods=["GET"], url_path="group-paramtros", name="agrupar paramtros")
    @permission_classes([AllowAnonymous])        
    def group_parametros_consignaciones(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            users = self.service.get_group_parametros()

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

            return True
        except Exception as e:
            raise e
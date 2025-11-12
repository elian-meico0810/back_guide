from datetime import datetime, timedelta
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from urllib.parse import quote
from mimetypes import guess_type
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from meicobaseapi.core.helpers.utils import formatErrors
from meicobaseapi.core.jwt_auth import JWTAuthentication
from meicobaseapi.core.pagination.custom_pagination import PaginationHandlerMixin, ResultsSetPagination
from meicobaseapi.core.permisions_decorator import has_required_permission
from meicobaseapi.domain.Consignaciones.consignaciones_services import ConsignacionesService
from meicobaseapi.core.APIResponse import APIResponse
from meicobaseapi.core.authentication import AllowAnonymous
from meicobaseapi.enums.GoAnWhere.gaw_enum import CredencialesAzure
from meicobaseapi.interface.Consignaciones.consignaciones_serializers import ConsignacionesListSerializer, ConsignacionesSerializer
from rest_framework.decorators import action, permission_classes
 
class ConsignacionesViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    service =  ConsignacionesService()
    # Definimos el serializador primcipal
    serializer_class = ConsignacionesSerializer
    # Definimos el serializador para listas primicipal
    list_serializer_class = ConsignacionesListSerializer
    # Aplicamos la paginacion
    pagination_class = ResultsSetPagination
    # Validamos la autentiacion
    authentication_classes= [JWTAuthentication]
 

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
    @action(detail=False, methods=["GET"], url_path="group-paramtros", name="agrupar paramtros",
    permission_classes=[has_required_permission(['0001'])])
    def group_parametros_consignaciones(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            data = self.service.get_group_parametros()

            paginator = self.pagination_class()

            page = request.query_params.get("page", None)
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
    @action(detail=False, methods=["DELETE"], url_path="eliminar", name="Eliminar adjunto de consignacion")
    def eliminar_consignacion(self, request):
        try:
            pk = request.query_params.get("id", None)
            if not pk:
                return APIResponse.error(message="El ID de la consignacion es requerido.", data={})
            
            self.service.destroy(pk)
            
            return APIResponse.successful(message="Operación exitosa", data=[])
        except Exception as e:
            return APIResponse.failed(e)
        
        
    @swagger_auto_schema(tags=["consignaciones"])
    @action(detail=False, methods=["POST"], url_path="public-azure", name="publicar ruta temporal de azure")        
    def public_azure(self, request):
        try:
            connection_string = CredencialesAzure.STOREGE_AZURE.value
            container_name = CredencialesAzure.CONTAINER_AZURE_DEV.value
            base_url = CredencialesAzure.BASE_URL_AZURE.value

            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            container_client = blob_service_client.get_container_client(container_name)

            nombre = request.data.get('file_nombre')
            folder = request.data.get('folder')

            if not nombre or not folder:
                raise Exception("El nombre y el folder son requeridos.")

            blob_name = f"{folder}/{nombre}"

            # Detecta el tipo MIME según la extensión
            mime_type, _ = guess_type(nombre)
            mime_type = mime_type or "application/octet-stream"

            # 🔹 Generar SAS incluyendo los encabezados de respuesta
            sas_token = generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=blob_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True),
                expiry=datetime.utcnow() + timedelta(minutes=10),
                content_disposition="inline",
                content_type=mime_type       
            )

            # Asegúrate de que base_url no tenga duplicado el contenedor
            if base_url.endswith(container_name):
                url_base = base_url
            else:
                url_base = f"{base_url}/{container_name}"

            url_sas = f"{url_base}/{quote(blob_name)}?{sas_token}"

            return APIResponse.successful(
                message="Operación exitosa, SAS generado por 10 minutos",
                data={"url_sas": url_sas}
            )
        except Exception as e:
            return APIResponse.error(message=str(e))
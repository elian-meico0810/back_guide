from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.decorators import permission_classes
from meicobaseapi.core.helpers.utils import formatErrors
from meicobaseapi.core.pagination.custom_pagination import PaginationHandlerMixin, ResultsSetPagination
from meicobaseapi.domain.Roles.roles_services import RolesService
from meicobaseapi.core.APIResponse import APIResponse
from meicobaseapi.core.authentication import AllowAnonymous
from meicobaseapi.core.jwt_auth import JWTAuthentication
from meicobaseapi.interface.Roles.roles_serializers import RolesSerializer, UsuariosListSerializer, RolesUpdatedSerializer


class RolesViewSet(viewsets.ViewSet, PaginationHandlerMixin):
    service = RolesService()
    # Definimos el serializador primcipal
    serializer_class = RolesSerializer
    # Definimos el serializador para listas primicipal
    list_serializer_class = UsuariosListSerializer
    # Aplicamos la paginacion
    pagination_class = ResultsSetPagination


    @swagger_auto_schema(tags=["groups"])
    @action(detail=False, methods=["GET"], url_path="obtener", name="Obtener rooles")
    @permission_classes([AllowAnonymous])
    def obtener_roles(self, request):
        try:
            # Obtenemos el queryset desde el servicio
            users = self.service.get_all_roles()

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


    @swagger_auto_schema(tags=["groups"])
    @action(detail=False, methods=["POST"], url_path="crear", name="Crear un rol")
    @permission_classes([AllowAnonymous])
    def crear_rol(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                self.service.create_role(request.data)
            else:
                return APIResponse.failed(error=formatErrors(serializer.errors))
             
            return APIResponse.successful(message="Operación exitosa", data=[])
        except Exception as e:
            return APIResponse.failed(e)


    @swagger_auto_schema(tags=["groups"])
    @action(detail=False, methods=["PUT"], url_path="actualizar", name="Modificar un rol")
    def actualizar_rol(self, request):
        try:
            id = request.query_params.get("id", None)
            if not id:
                return APIResponse.error(message="El ID del rol es requerido.", data={})
            
            nombre = request.data.get("nombre", None)
            user_data = request.user
            data = None
            auth_user = self.service.get_role_by_id(id)
            serializer = RolesUpdatedSerializer(data=request.data)
            if serializer.is_valid():
                usuario = self.service.get_role_by_name(nombre)
                usuario_actualizado = self.service.update_role(usuario, auth_user, request.data)
                data = RolesUpdatedSerializer(usuario_actualizado).data
            else:
                print("serializer errors:", serializer.errors)
                return APIResponse.failed(error=formatErrors(serializer.errors))
    
            return APIResponse.successful(
                message="Usuario actualizado correctamente",
                data=data
            )
        except Exception as e:
            return APIResponse.failed(e)
    

    @swagger_auto_schema(tags=["groups"])
    @action(detail=False, methods=["DELETE"], url_path="eliminar", name="Eliminar un rol")
    def eliminar_rol(self, request):
        try:
            pk = request.query_params.get("id", None)
            if not pk:
                return APIResponse.error(message="El ID del rol es requerido.", data={})
            
            data = self.service.get_role_by_id(pk)
            if not data:
                return APIResponse.error(message="Usuario no encontrado.", data={})
            
            self.service.delete_role(pk)
            
            return APIResponse.successful(message="Operación exitosa", data=[])
        except Exception as e:
            return APIResponse.failed(e)

    
    @authentication_classes([JWTAuthentication])
    @swagger_auto_schema(tags=["groups"])
    @action(detail=False, methods=["GET"], url_path="getRolById", name="Obtener un rol especifico")
    def get_rol_by_id(self, request):
        try:
            rol_id = request.query_params.get("rol_id", None)
            if not rol_id:
                return APIResponse.error(message="El ID del rol es requerido.", data={})
            
            data = self.service.get_role_by_id(rol_id)
            serializer = RolesSerializer(data)
            return APIResponse.successful(message="Datos obentenidos con exito.", data=serializer.data)
        except Exception as e:
            return APIResponse.failed(e)
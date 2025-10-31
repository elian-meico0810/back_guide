from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes, authentication_classes
from drf_yasg.utils import swagger_auto_schema
from meicobaseapi.core.helpers.utils import formatErrors
from meicobaseapi.core.pagination.custom_pagination import BasicPagination
from .usuarios_serializers import UsersariosUpdatedSerializer, UsuariosSerializer, UsuariosListSerializer
from meicobaseapi.domain.Usuarios.usuarios_services import UsuariosService
from meicobaseapi.core.APIResponse import APIResponse
from rest_framework.decorators import permission_classes
from meicobaseapi.core.authentication import AllowAnonymous
from meicobaseapi.core.jwt_auth import JWTAuthentication


class UsuariosViewSet(viewsets.ViewSet):
    #Obtenemos el serivico de usuarios
    service = UsuariosService()
    # Definimos el serializador primcipal
    serializer_class = UsuariosSerializer
    # Definimos el serializador para listas primicipal
    list_serializer_class = UsuariosListSerializer
    # Aplicamos la paginacion
    pagination_class = BasicPagination


    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["GET"], url_path="obtener", name="Obtener Usuarios")
    @permission_classes([AllowAnonymous])
    def obtener_usuarios(self, request):
        try:
            users = self.service.get_all_users()
            page = request.query_params.get("page", None)
            # Inicializamos variables
            data = None

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(users, request)
            
            if page:
                serializer = self.list_serializer_class(page, many=True)
                data = paginator.get_paginated_response(serializer.data).data
            else:
                serializer = self.list_serializer_class(users, many=True)
                data = serializer.data

            return APIResponse.successful(
                message="Operación exitosa",
                data=data
            )
        except Exception as e:
            return APIResponse.failed(e)


    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["POST"], url_path="crear", name="Crear un usuario")
    @permission_classes([AllowAnonymous])
    def crear_usuario(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                self.service.create_user(request.data)
            else:
                return APIResponse.failed(error=formatErrors(serializer.errors))
             
            return APIResponse.successful(message="Operación exitosa", data=[])
        except Exception as e:
            return APIResponse.failed(e)


    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["PUT"], url_path="actualizar", name="Modificar un usuario")
    def actualizar_usuario(self, request):
        try:
            id = request.query_params.get("id", None)
            if not id:
                return APIResponse.error(message="El ID de usuario es requerido.", data={})
            
            user_data = request.user
            data = None
            auth_user = self.service.get_user_by_id(id)
            serializer = UsersariosUpdatedSerializer(data=request.data)
            if serializer.is_valid():
                usuario = self.service.get_user_by_email(auth_user.correo)
                usuario_actualizado = self.service.update_user(usuario, auth_user, request.data)
                data = UsersariosUpdatedSerializer(usuario_actualizado).data
            else:
                return APIResponse.failed(error=formatErrors(serializer.errors))
    
            return APIResponse.successful(
                message="Usuario actualizado correctamente",
                data=data
            )
        except Exception as e:
            return APIResponse.failed(e)
    

    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["DELETE"], url_path="eliminar", name="Eliminar un usuario")
    def eliminar_usuario(self, request):
        try:
            pk = request.query_params.get("id", None)
            if not pk:
                return APIResponse.error(message="El ID de usuario es requerido.", data={})
            
            data = self.service.get_user_by_id(pk)
            if not data:
                return APIResponse.error(message="Usuario no encontrado.", data={})
            
            self.service.delete_user(pk)
            
            return APIResponse.successful(message="Operación exitosa", data=[])
        except Exception as e:
            return APIResponse.failed(e)

    
    @authentication_classes([JWTAuthentication])
    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["GET"], url_path="getUser", name="Obtener un usuario especifico")
    def get_user_by_id(self, request):
        try:
            user_id = request.query_params.get("user_id", None)
            if not user_id:
                return APIResponse.error(message="El ID de usuario es requerido.", data={})
            
            users = self.service.get_user_by_id(user_id)
            serializer = UsuariosSerializer(users)
            return APIResponse.successful(message="Datos obentenidos con exito.", data=serializer.data)
        except Exception as e:
            return APIResponse.failed(e)


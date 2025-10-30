from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes, authentication_classes
from drf_yasg.utils import swagger_auto_schema
from .usuarios_serializers import UsuariosSerializer
from meicobaseapi.domain.Usuarios.usuarios_services import UsuariosService
from meicobaseapi.core.APIResponse import APIResponse
from rest_framework.decorators import permission_classes
from meicobaseapi.core.authentication import AllowAnonymous
from meicobaseapi.core.jwt_auth import JWTAuthentication


class UsuariosViewSet(viewsets.ViewSet):
    service = UsuariosService()

    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["get"], url_path="obtener", name="Obtener Usuarios")
    @permission_classes([AllowAnonymous])
    def obtener_usuarios(self, request):
        users = self.service.get_all_users()
        serializer = UsuariosSerializer(users, many=True)
        return APIResponse(status.HTTP_200_OK, serializer.data, "Operación exitosa")

    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["post"], url_path="crear", name="Crear un usuario")
    @permission_classes([AllowAnonymous])
    def crear_usuario(self, request):
        try:
            print(request.data["Usuario"])
            self.service.create_user(request.data["Usuario"])
            return APIResponse(status.HTTP_200_OK, True, "Operación exitosa")
        except Exception as e:
            return APIResponse(status.HTTP_500_INTERNAL_SERVER_ERROR, False, "Ha ocurrido un error")

    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["put"], url_path="actualizar", name="Modificar un usuario")
    def actualizar_usuario(self, request):
        user_data = request.user
        auth_user = self.service.get_user_by_email(user_data['email'])

        if not auth_user:
            return APIResponse(status.HTTP_404_NOT_FOUND, None, "Usuario autenticador no encontrado")
        
        usuario_data = request.data.get("Usuario", {})
        new_usuario_data = usuario_data.get("newUser", {})
        usuario_correo = new_usuario_data.get("correo", None)   
        nuevo_estado = usuario_data.get("estado", None)

        usuario = self.service.get_user_by_email(usuario_correo)

        usuario.area = new_usuario_data["area"]
        usuario.cargo = new_usuario_data["cargo"]
        usuario.celular = new_usuario_data["celular"]
        usuario.ciudad = new_usuario_data["ciudad"]
        usuario.correo = new_usuario_data["correo"]
        usuario.nombre = new_usuario_data["nombre"]
        self.service.update_user(usuario, nuevo_estado, auth_user)

        if not usuario:
            return APIResponse(status.HTTP_404_NOT_FOUND, None, "Usuario no encontrado")
        
        usuario_serializado = UsuariosSerializer(usuario).data
        return APIResponse(status.HTTP_200_OK, usuario_serializado, "Usuario actualizado correctamente")

    @swagger_auto_schema(tags=["users"])
    @action(detail=True, methods=["delete"], url_path="eliminar", name="Eliminar un usuario")
    def eliminar_usuario(self, request, pk):
        self.service.delete_user(pk)
        return APIResponse(status.HTTP_200_OK, True, "Operación exitosa")
    
    @authentication_classes([JWTAuthentication])
    @swagger_auto_schema(tags=["users"])
    @action(detail=False, methods=["post"], url_path="getUser", name="Obtener un usuario especifico")
    def get_user_by_id(self, request):
        try:
            user_id = request.data.get("user_id")
            if user_id is not None:
                users = self.service.get_user_by_id(user_id)
                serializer = UsuariosSerializer(users)
                return APIResponse(status.HTTP_200_OK, serializer.data, "OK")
            return APIResponse(status.HTTP_400_BAD_REQUEST, None, "El campo user_id debe ser enviado")
        except Exception as e:
            return APIResponse(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                '',
                message=f"Error: {str(e)}",
            )

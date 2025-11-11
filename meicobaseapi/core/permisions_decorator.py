from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from meicobaseapi.core.authentication import TokenValidate

class MeicoPermissionDenied(PermissionDenied):
    pass

class HasRequiredPermission(BasePermission):
    def __init__(self, required_permissions):
        self.required_permissions = required_permissions
        self.validateService = TokenValidate()

    def has_permission(self, request, view):
        try:
            auth_result = self.validateService.authenticate(request)
            if auth_result is None:
                raise MeicoPermissionDenied('No estás autenticado.')

            token_data = auth_result[0]  # ahora seguro
            permisos_token = token_data.get('permissions', [])
            print(
                "required_permissions: ",self.required_permissions,
                "permisos_token: ",permisos_token,
            )
            for permiso in self.required_permissions:
                if permiso in permisos_token:
                    return True

            raise MeicoPermissionDenied('No tienes los permisos necesarios para acceder a este recurso.')
        except Exception as e:
            raise e



def has_required_permission(required_permissions):
    class MeicoPermission(HasRequiredPermission):
        def __init__(self):
            super().__init__(required_permissions)

        def has_permission(self, request, view):
            return super().has_permission(request, view)

    return MeicoPermission


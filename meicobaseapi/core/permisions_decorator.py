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
        #token_data = request.auth
        token_data = self.validateService.authenticate(request)[0]
        if not token_data:
            raise MeicoPermissionDenied('No estás autenticado.')

        permisos_token = token_data.get('permissions', [])
        for permiso in self.required_permissions:
            if permiso in permisos_token:
                return True

        raise MeicoPermissionDenied('No tienes los permisos necesarios para acceder a este recurso.')

def has_required_permission(required_permissions):
    class MeicoPermission(HasRequiredPermission):
        def __init__(self):
            super().__init__(required_permissions)

        def has_permission(self, request, view):
            return super().has_permission(request, view)

    return MeicoPermission


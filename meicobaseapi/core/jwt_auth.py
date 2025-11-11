import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from meicobaseapi.core.MeicoUser import Meico_User

class MeicoAuthenticationFailed(AuthenticationFailed):
    pass

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        try:
            prefix, token = auth_header.split(' ')
            if prefix.lower() != 'bearer':
                raise MeicoAuthenticationFailed('Token inválido')
        except ValueError:
            raise MeicoAuthenticationFailed('Formato de token inválido')

        try:
            payload = jwt.decode(token, settings.SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise MeicoAuthenticationFailed('El token ha expirado')
        except jwt.InvalidTokenError:
            raise MeicoAuthenticationFailed('Token inválido')

        username = payload.get('user_name')
        username = username.split('@')[0]
        email = payload.get('email')
        display_name = payload.get('display_name')
        user = Meico_User(username=username, email=email, display_name=display_name)

        request.user = user
        return (user, payload)

    def authenticate_header(self, request):
        return 'Bearer'

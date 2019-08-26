from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated


class TokenExpirationCheck(permissions.BasePermission):
    message = ''

    @staticmethod
    def _get_access_token(request):
        access_token = request.META['HTTP_AUTHORIZATION']
        if access_token.startswith('Bearer '):
            return access_token.replace('Bearer ', '')
        return access_token

    def has_permission(self, request, view):
        access_token = self._get_access_token(request)
        token_obj_list = Token.objects.filter(pk=access_token)
        if token_obj_list.exists():
            return True
        else:
            raise NotAuthenticated()

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsSuperuser, IsOwner
from .models import User
from .serializers import UserSerializer
from .paginations import Pagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    ordering_fields = ['create_at', 'is_active', 'is_superuser', 'is_staff']
    ordering = ['-create_at']

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            pass
        elif self.action == 'retrieve':
            pass
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwner | IsSuperuser]
        elif self.action in ['set_password', 'update_avatar']:
            permission_classes = [IsOwner | IsSuperuser]
        return [permission() for permission in permission_classes]

    # create user with avatar by post
    @parser_classes([MultiPartParser, FormParser])
    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    @parser_classes([MultiPartParser, FormParser])
    @action(detail=True, methods=['put'])
    def update_avatar(self, request, *args, **kwargs):
        return super(UserViewSet, self).partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def set_password(self, request, pk=None):
        user = request.user
        if user.check_password(request.data['oldPassword']):
            user.set_password(request.data['newPassword'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(data={'detail': '老密码输入不正确!'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_auth_user(self, request, pk=None):
        authentication = JWTAuthentication()
        user, _ = authentication.authenticate(request)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsSuperuser, IsOwner
from .models import User
from .serializers import UserSerializer, PasswordSerializer
from .paginations import Pagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username']
    ordering_fields = ['username']
    ordering = ['username']

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
        elif self.action == 'set_password':
            permission_classes = [IsAuthenticated | IsSuperuser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def get_auth_user(self, request, pk=None):
        authentication = JWTAuthentication()
        user, _ = authentication.authenticate(request)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

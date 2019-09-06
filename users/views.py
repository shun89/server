from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsSuperuser, IsOwner
from .models import User
from .serializers import UserSerializer, PasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        serializer = PasswordSerializer(data=request.data, context={'request': request})
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        request = self.request
        permission_classes = []
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'create':
            # 只有超级用户能创建员工
            is_create_staff = 'is_staff' in request.data and request.data['is_staff']
            is_create_superuser = 'is_superuser' in request.data and request.data['is_superuser']
            permission_classes = [IsSuperuser] if is_create_staff or is_create_superuser else []
        elif self.action == 'retrieve':
            pass
        elif self.action in ['update', 'partial_update', 'destroy']:
            object_user = self.get_object()
            if object_user.is_admin_user:
                permission_classes = [IsOwner | IsSuperuser]
            else:
                permission_classes = [IsOwner | IsAdminUser]
        elif self.action == 'set_password':
            permission_classes = [IsOwner | IsSuperuser]
        return [permission() for permission in permission_classes]

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperuser
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

    def _is_staff_action(self, request):
        if self.action == 'create':
            return request.data['is_staff']
        elif self.action in ['update', 'partial_update', 'destroy']:
            object_user = self.get_object()
            return object_user.is_staff
        return False

    def _is_general_user_udr(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            object_user = self.get_object()
            return not object_user.is_staff
        return False

    def get_permissions(self):
        permission_classes = []
        if self._is_staff_action(self.request):
            permission_classes = [IsSuperuser]
        elif self._is_general_user_udr():
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

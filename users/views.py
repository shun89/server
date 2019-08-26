from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

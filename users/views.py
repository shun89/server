from rest_framework import status, viewsets
from rest_framework.decorators import action, parser_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User
from .paginations import Pagination
from .permissions import IsOwner, IsSuperuser
from .serializers import (ResetPasswordSerializer, RetrievePasswordSerializer,
                          UserSerializer)
from .utils import extract_reset_password_user, gen_reset_password_email_html


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = Pagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["username"]
    ordering_fields = ["create_at", "is_active", "is_superuser", "is_staff"]
    ordering = ["-create_at"]

    def get_permissions(self):
        permission_classes = []
        if self.action in ["list", "reset_password"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["create", "retrieve", "retrieve_password"]:
            pass
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsOwner | IsSuperuser]
        elif self.action in ["set_password", "update_avatar"]:
            permission_classes = [IsOwner | IsSuperuser]
        return [permission() for permission in permission_classes]

    # create user with avatar by post
    @parser_classes([MultiPartParser, FormParser])
    def create(self, request, *args, **kwargs):
        return super(UserViewSet, self).create(request, *args, **kwargs)

    @parser_classes([MultiPartParser, FormParser])
    @action(detail=True, methods=["put"])
    def update_avatar(self, request, *args, **kwargs):
        return super(UserViewSet, self).partial_update(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def update_password(self, request, pk=None):
        user = request.user
        if user.check_password(request.data["oldPassword"]):
            user.set_password(request.data["newPassword"])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            data={"detail": "老密码输入不正确!"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["post"])
    def retrieve_password(self, request, pk=None):
        serializer = RetrievePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).first()
            agent = request.META["HTTP_USER_AGENT"]
            html_content = gen_reset_password_email_html(user, agent)
            user.receive_email("密码找回", html_content)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                data={"detail": "该邮箱没有注册!"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"])
    def reset_password(self, request, pk=None):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = extract_reset_password_user(serializer.data)
        user.set_password(serializer.data["password"])
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def get_auth_user(self, request, pk=None):
        authentication = JWTAuthentication()
        user, _ = authentication.authenticate(request)
        serializer = UserSerializer(user)
        message = 'abd'
        print mesage
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)

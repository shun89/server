from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from server import settings
from users.urls import urlpatterns as users_url

urlpatterns = [
    path("api/token_auth/", TokenObtainPairView.as_view(), name="token-auth"),
    path("api/token_verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("api/token_refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "openapi/",
        get_schema_view(title="Server", description="api for server", version="1.0.0"),
        name="openapi-schema",
    ),
    path(
        "redoc/",
        TemplateView.as_view(
            template_name="index.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="redoc",
    ),
    path("api/", include((users_url, "users"))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

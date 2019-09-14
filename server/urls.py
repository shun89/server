from django.urls import path
from django.conf.urls import include
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from users.urls import urlpatterns as users_url
from django.conf.urls.static import static
from server import settings

urlpatterns = [
    path('api/token_auth/', obtain_jwt_token),
    path('api/token_verify/', verify_jwt_token),
    path('api/token_refresh/', refresh_jwt_token),
    path('api/', include((users_url, 'users'))),
    path('openapi/', get_schema_view(
        title='Server',
        description='api for server',
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger/', TemplateView.as_view(
        template_name='index.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
] + static(settings.STATIC_URL)

from django.urls import path
from django.conf.urls import include
from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token
)
from users.urls import urlpatterns as accounts_url


urlpatterns = [
    path('api/token_auth/', obtain_jwt_token),
    path('api/token_verify/', verify_jwt_token),
    path('api/token_refresh/', refresh_jwt_token),
    path('api/', include(accounts_url, 'users')),
]

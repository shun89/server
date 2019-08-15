from django.contrib.auth.backends import ModelBackend
from .models import User


class CameraBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        user = User.objects.get(username=kwargs['username'])
        if not user.check_password(kwargs['password']):
            raise Exception('password incorrect!')
        return user

from django.contrib.auth.backends import ModelBackend
from .models import User


class CameraBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        """自定义验证后端
        参数:
            username: 用户名
            password: 密码
        返回:
            自定义user
        异常:

        """
        user = User.objects.get(username=kwargs['username'])
        if not user.check_password(kwargs['password']):
            raise Exception('密码错误!')
        if user.role.is_leader() or user.role.is_cleaner():
            if user.staff.region.id != kwargs['region']:
                raise Exception('区域不匹配!')
        return user

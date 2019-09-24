import sys
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from .models import User
        from django.contrib.auth.models import Group
        from .constants import EVERYONE_GROUP, ANONYMOUS_GROUP, USERS_GROUP, STAFFS_GROUP, SUPERUSERS_GROUP
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'zhongshun6666@163.com', '123456')
        Group.objects.get_or_create(name=EVERYONE_GROUP)
        Group.objects.get_or_create(name=ANONYMOUS_GROUP)
        Group.objects.get_or_create(name=USERS_GROUP)
        Group.objects.get_or_create(name=STAFFS_GROUP)
        Group.objects.get_or_create(name=SUPERUSERS_GROUP)

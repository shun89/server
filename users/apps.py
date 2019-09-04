import sys
from django.apps import AppConfig
from django.contrib.auth.models import Group


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from .constants import GROUP_EVERYONE, GROUP_ANONYMOUS, GROUP_USERS, GROUP_STAFFS
        Group.objects.get_or_create(name=GROUP_EVERYONE)
        Group.objects.get_or_create(name=GROUP_ANONYMOUS)
        Group.objects.get_or_create(name=GROUP_USERS)
        Group.objects.get_or_create(name=GROUP_STAFFS)


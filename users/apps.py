from django.apps import AppConfig
from django.contrib.auth.models import Group


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from .constants import EVERYONE_GROUP, ANONYMOUS_GROUP, USERS_GROUP, STAFFS_GROUP, SUPERUSERS_GROUP
        Group.objects.get_or_create(name=EVERYONE_GROUP)
        Group.objects.get_or_create(name=ANONYMOUS_GROUP)
        Group.objects.get_or_create(name=USERS_GROUP)
        Group.objects.get_or_create(name=STAFFS_GROUP)
        Group.objects.get_or_create(name=SUPERUSERS_GROUP)


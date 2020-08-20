from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .constants import *


@receiver(post_save, sender=User)
def user_post_save(sender):
    sender.groups.clear()
    if sender.is_superuser:
        superusers_group = Group.objects.get(name=SUPERUSERS_GROUP)
        sender.groups.add(superusers_group)
    elif sender.is_staff:
        staffs_group = Group.objects.get(name=STAFFS_GROUP)
        sender.groups.add(staffs_group)
    elif sender.is_anonymous:
        anonymous_group = Group.objects.get(name=ANONYMOUS_GROUP)
        sender.groups.add(anonymous_group)
    else:
        users_group = Group.objects.get(name=USERS_GROUP)
        sender.groups.add(users_group)
    everyone_group = Group.objects.get(name=EVERYONE_GROUP)
    sender.groups.add(everyone_group)

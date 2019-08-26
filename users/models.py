from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import (
    UserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=timezone.now)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

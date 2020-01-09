from django.db import models
from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth.models import (
    UserManager,
    AbstractBaseUser,
    PermissionsMixin
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/user-default.png')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def receive_email(self, subject, html_content, from_email=None):
        msg = EmailMessage(subject, html_content, from_email, [self.email])
        msg.content_subtype = 'html'
        msg.send()


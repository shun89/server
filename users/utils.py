from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer
from django.conf import settings
from rest_framework.exceptions import NotFound
from .models import User


def gen_reset_password_email_html(user, agent):
    token = TokenObtainSlidingSerializer.get_token(user)
    user_id = urlsafe_base64_encode(force_bytes(user.id))
    url = f"{settings.FRONTEND_RESET_PASSWORD_PAGE}/?userId={user_id}&token={token}"
    return render_to_string(
        "reset_password_template.html",
        {
            "username": user.username,
            "timeout": f'{int(settings.SIMPLE_JWT["SLIDING_TOKEN_LIFETIME"].seconds/60)}分钟',
            "agent": agent,
            "reset_url": url,
        },
    )


def extract_reset_password_user(data):
    user_id = force_text(urlsafe_base64_decode(data["user_id"]))
    user = User.objects.filter(pk=user_id).first()
    if user:
        return user
    else:
        raise NotFound()

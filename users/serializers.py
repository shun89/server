from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(self.initial_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        exclude = ["password"]


class RetrievePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=200)
    password = serializers.CharField(min_length=6)

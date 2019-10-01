from rest_framework import serializers
from .models import User


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6)

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password']

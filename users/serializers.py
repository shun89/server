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

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(self.initial_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        exclude = ['password']

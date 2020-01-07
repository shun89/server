from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(self.initial_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        exclude = ['password']

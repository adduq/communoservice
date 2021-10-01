from rest_framework import serializers
from .models import UserInfo
from django.contrib.auth.models import User


class UserInfoSerializer(serializers.ModelSerializer):

    def validate_creation(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(user_id=value).exists():
            raise serializers.ValidationError('already exists')
        return value

    class Meta:
        model = UserInfo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
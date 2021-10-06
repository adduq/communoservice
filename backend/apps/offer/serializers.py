from rest_framework import serializers
from .models import Offer
from django.contrib.auth.models import User


class OfferSerializer(serializers.ModelSerializer):

    def validate_creation(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(user=value).exists():
            raise serializers.ValidationError('already exists')
        return value

    class Meta:
        model = Offer
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

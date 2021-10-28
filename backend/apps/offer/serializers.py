from rest_framework import serializers
from .models import Offer, ServiceType
from django.contrib.auth.models import User
from datetime import date


class OfferSerializer(serializers.ModelSerializer):

    def validate_creation(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(user=value).exists():
            raise serializers.ValidationError('already exists')
        return value

    def validate_expiration_date(self, value):
        if value is not None:
            if value < date.today():
                raise serializers.ValidationError(
                    "Expiration date is not valid.")
            return value

    class Meta:
        model = Offer
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

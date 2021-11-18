from django.db import models
from django.db.models import fields
from rest_framework import serializers

from apps.userinfo.serializers import UserSerializer
from .models import ActiveOffer, Offer, ReservedOffer, TerminatedOffer, ServiceType
from django.contrib.auth.models import User
from datetime import date


class OfferSerializer(serializers.ModelSerializer):

    def validate_creation(self, value):
        ModelClass = self.Meta.model
        if ModelClass.objects.filter(user=value).exists():
            raise serializers.ValidationError('already exists')
        return value

    def validate_end_date(self, value):
        if value is not None:
            if value < date.today():
                raise serializers.ValidationError(
                    "End date is not valid.")
            return value

    def validate_start_date(self, value):
        if value is not None:
            if value < date.today():
                raise serializers.ValidationError(
                    "Start date is not valid.")
            return value

    def validate_date_range(self, start, end):
        if start is not None & end is not None:
            if start > end:
                raise serializers.ValidationError(
                    "Start date must be before end date.")
            return

    class Meta:
        model = Offer
        fields = '__all__'


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


class ActiveOfferCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveOffer
        fields = '__all__'


class ActiveOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveOffer
        fields = '__all__'
        depth = 1


class ReservedOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedOffer
        fields = '__all__'
        depth = 1


class ReservedOfferCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservedOffer
        fields = '__all__'


class TerminatedOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminatedOffer
        fields = '__all__'
        depth = 1


class TerminatedOfferCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminatedOffer
        fields = '__all__'

from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta


class Offer(models.Model):
    user = models.ForeignKey(
        User, related_name='offers', db_column="id_user", on_delete=models.CASCADE)
    type_service = models.CharField(max_length=30, default="Administration")
    description = models.CharField(
        null=True, max_length=100, default="Aucune description")
    hourly_rate = models.DecimalField(
        null=True, max_digits=6, decimal_places=2)
    max_distance = models.PositiveIntegerField(null=True)
    date_added = models.DateField(auto_now_add=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True)

    class Meta:
        ordering = ('-date_added',)


class ServiceType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'  # le f permet de formatter.

    # pour test
    def get_name(self):
        return self.name

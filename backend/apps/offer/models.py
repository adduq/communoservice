from django.db import models
from django.contrib.auth.models import User


class Offer(models.Model):
    user = models.ForeignKey(
        User, related_name='offers', db_column="id_user", on_delete=models.CASCADE)
    type_service = models.CharField(max_length=30, default="Administration")
    description = models.CharField(
        null=True, max_length=100, default="Aucune description")
    hourly_rate = models.DecimalField(
        null=True, max_digits=6, decimal_places=2)
    max_distance = models.PositiveIntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)

from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user_id = models.ForeignKey(
        User, related_name='offers', db_column="id_user", on_delete=models.CASCADE)

    nb_services_done = models.PositiveIntegerField(null=True)

    profile_is_completed = models.BooleanField(default=False)

    user_is_worker = models.BooleanField(default=False)

    user_is_employer = models.BooleanField(default=False)

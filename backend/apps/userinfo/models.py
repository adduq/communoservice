from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, to_field="id")

    profile_is_completed = models.BooleanField(default=False)

    first_name = models.CharField(max_length=30)

    last_name = models.CharField(max_length=30)

    email = models.EmailField()

    nb_services_received = models.PositiveIntegerField(null=False)

    nb_services_given = models.PositiveIntegerField(null=False)

    avg_rating_as_employee = models.DecimalField(decimal_places=2,
                                                 max_digits=3,
                                                 null=False,
                                                 default=0)

    nb_rating_as_employe = models.PositiveIntegerField(null=False, default=0)

    avg_rating_as_employer = models.DecimalField(decimal_places=2,
                                                 max_digits=3,
                                                 null=False,
                                                 default=0)

    nb_rating_as_employer = models.PositiveIntegerField(null=False, default=0)

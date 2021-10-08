from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging
import pprint

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    print('Logged in')
    pprint(vars(user))
    userinfo = UserInfo.objects.get(user_id=request.user.user_id)
    pprint(vars(userinfo))
    # userinfo.is_online = True
    # userinfo.save()

@receiver(user_logged_out)
def got_offline(request, user, **kwargs):   
    print('Logged off')
    pprint(vars(user))
    userinfo = UserInfo.objects.get(user_id=request.user.user_id)
    pprint(vars(userinfo))
    # userinfo.is_online = False
    # userinfo.save()

class UserInfo(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, to_field="id")

    is_online = models.BooleanField(default=False)

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

    user_bio = models.CharField(max_length=150)

    location_lat = models.CharField(max_length=15)

    location_lon = models.CharField(max_length=15)

    address = models.CharField(max_length=100)
import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def login_logger(request, user, **kwargs):
    print('Logged in')

@receiver(user_logged_out)
def got_offline(request, user, **kwargs):   
    print('Logged off')

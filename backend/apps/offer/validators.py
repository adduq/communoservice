from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta
from pprint import pprint

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_expiration_date(self, value):
    
    pprint(value)
    print(value)
    if value < date.today:
        raise ValidationError(
            _('Expiration date is not valid.'),
            params={'value': value},
        )

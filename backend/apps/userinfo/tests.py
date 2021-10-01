import unittest
from django.test import RequestFactory, TestCase

from django.core.exceptions import *
from django.db.utils import IntegrityError
from django.db import DataError
from django.contrib.auth.models import User
from .models import UserInfo
#from .fixtures import OfferFixtures
from .views import UserInfoDetail
from pprint import pprint


'''https://www.geeksforgeeks.org/python-assertion-error/'''

'''Tests du model UserInfo'''

# Tester le trigger dans la BD

class TestOffer(unittest.TestCase):
    pass
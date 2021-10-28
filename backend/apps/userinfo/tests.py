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
class UserInfo(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_givenNullUser_whenCreatingInstance_thenExpectError(self):

        # given
        pass

    def test_givenNullTypeService_whenCreatingInstance_thenExpectError(self):

        # given
        pass

    def test_givenNullDescription_whenCreatingInstance_thenExpectError(self):

        # given


        # when

        # then
        pass

    def test_givenBlankDescription_whenCreatingInstance_thenReturnValidInstance(self):

        # given

        # when

        # then
        pass

    def test_givenNegativeRate_whenCreatingInstance_thenExpectError(self):

        # given


        # when

        # then
        pass

    def test_givenRateDigitsGreaterThanMaxDigits_whenCreatingInstance_thenExpectError(self):

        # given

        # then
        pass

    def test_givenRateDecimalsGreaterThanMaxDecimals_whenCreatingInstance_thenExpectError(self):

        # given


        # when

        # then
        pass

    def test_givenNegativeDistance_whenCreatingInstance_thenExpectError(self):

        # given

        # then
        pass

    def test_givenPastExpirationDate_whenCreatingInstance_thenExpectError(self):
        # given

        # then
        pass

    def test_givenNoExpirationDate_whenCreatingInstance_thenReturnNewInstance(self):

        # given

        # when


        # then

        pass

    def test_givenNoDisponibilies_whenCreatingInstance_thenReturnNewInstance(self):

        # given

        # when

        # then
        pass

    def test_givenExistingOfferId_whenCreatingInstance_expectError(self):
        pass



'''Tests des endpoints'''


class OfferViewTest(TestCase):
    def setUp(self):
        pass

    def test_OffersView_whenGetMethod_thenResponseStatusCode200(self):
        # given


        # when


        # then
        pass

    def test_OffersView_whenIllegalPutMethod_thenResponseStatusCode405(self):
        # given


        # when


        # then
        pass

    def test_OffersView_whenCreateOffer_thenResponseStatusCode201(self):

        # given

        # when

        # then
        pass

    def test_OffersView_whenCreateOfferWithNonExistentUser_thenResponseStatusCode400(self):

        # given

        # when

        # then
        pass

    def test_OffersView_whenCreateOfferWithPastExpirationDate_thenResponseStatusCode400(self):

        # given

        # when

        # then
        pass
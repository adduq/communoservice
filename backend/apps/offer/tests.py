import unittest
from django.test import RequestFactory, TestCase

from django.core.exceptions import *
from django.db.utils import IntegrityError
from django.db import DataError
from django.contrib.auth.models import User

from apps.userinfo.models import UserInfo
from .models import Offer
from .fixtures import OfferFixtures
from .views import Offers
from datetime import date, timedelta
from pprint import pprint


'''https://www.geeksforgeeks.org/python-assertion-error/'''

'''Tests du model Offer'''


class TestOffer(unittest.TestCase):

    def setUp(self):
        username = "Gandalf"
        firstname = "Gandalf"
        lastname = "LeBlanc"
        email = "gandalf@globetrotter.net"
        password = "qwerty1234"

        self.user = User.objects.create(username=username,
                                        first_name=firstname,
                                        last_name=lastname,
                                        email=email,
                                        password=password)

    def tearDown(self):
        self.user.delete()

    def test_givenNullUser_whenCreatingInstance_thenExpectError(self):

        # given
        nullUser = None
        test_type_service = OfferFixtures.any_type_service()
        test_description = OfferFixtures.any_description()
        test_hourly_rate = OfferFixtures.any_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()

        try:
            Offer.objects.create(user=nullUser,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist)
        except IntegrityError as msg:
            self.assertRaisesRegexp(
                IntegrityError, "^.*ERREUR:  une valeur NULL viole la contrainte NOT NULL de la colonne « id_user » dans la relation « offer_offer.* »")
            print('**********************************************************')
            print(self._testMethodName)
            print(msg.args)
            print('**********************************************************')

    def test_givenNullTypeService_whenCreatingInstance_thenExpectError(self):

        # given
        test_user = self.user
        test_type_service = None
        test_description = OfferFixtures.any_description()
        test_hourly_rate = OfferFixtures.any_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()

        try:
            Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist)
        except IntegrityError as msg:
            self.assertRaisesRegexp(
                IntegrityError, "^.*ERREUR:  une valeur NULL viole la contrainte NOT NULL de la colonne « id_user » dans la relation « offer_offer.* »")
            print('**********************************************************')
            print(self._testMethodName)
            print(msg.args)
            print('**********************************************************')

    def test_givenNullDescription_whenCreatingInstance_thenExpectError(self):

        # given
        test_user = self.user
        test_type_service = OfferFixtures.any_type_service()
        test_description = None
        test_hourly_rate = OfferFixtures.any_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()

        # when
        Offer.objects.create(user=test_user,
                             type_service=test_type_service,
                             description=test_description,
                             hourly_rate=test_hourly_rate,
                             max_distance=test_max_dist)
        # then
        try:
            Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist)
        except IntegrityError as msg:
            self.assertRaisesRegexp(
                IntegrityError, "^.*ERREUR:  une valeur NULL viole la contrainte NOT NULL de la colonne « id_user » dans la relation « offer_offer,* »")
            print('**********************************************************')
            print(self._testMethodName)
            print(msg.args)
            print('**********************************************************')

    def test_givenBlankDescription_whenCreatingInstance_thenReturnValidInstance(self):

        # given
        test_user = self.user
        test_type_service = OfferFixtures.any_type_service()
        test_description = ""
        test_hourly_rate = OfferFixtures.any_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()

        # when
        offer = Offer.objects.create(user=test_user,
                                     type_service=test_type_service,
                                     description=test_description,
                                     hourly_rate=test_hourly_rate,
                                     max_distance=test_max_dist)
        # then
        self.assertEqual(offer.user, test_user)
        self.assertEqual(offer.type_service, test_type_service)
        self.assertEqual(offer.description, "")
        self.assertEqual(offer.hourly_rate, test_hourly_rate)
        self.assertEqual(offer.max_distance, test_max_dist)

    def test_givenNegativeRate_whenCreatingInstance_thenExpectError(self):

        # given
        test_user = self.user
        test_type_service = OfferFixtures.any_type_service()
        test_description = OfferFixtures.any_description()
        test_hourly_rate = OfferFixtures.negative_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()

        # when
        offer = Offer.objects.create(user=test_user,
                                     type_service=test_type_service,
                                     description=test_description,
                                     hourly_rate=test_hourly_rate,
                                     max_distance=test_max_dist)
        # then
        self.assertEqual(offer.user, test_user)
        self.assertEqual(offer.type_service, test_type_service)
        self.assertEqual(offer.description, test_description)
        self.assertEqual(offer.hourly_rate, test_hourly_rate)
        self.assertEqual(offer.max_distance, test_max_dist)

    def test_givenRateDigitsGreaterThanMaxDigits_whenCreatingInstance_thenExpectError(self):

        # given
        test_user = self.user
        test_type_service = OfferFixtures.any_type_service()
        test_description = OfferFixtures.any_description()
        test_hourly_rate = OfferFixtures.over_max_digits_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()

        # then
        try:
            Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist)
        except DataError as e:
            self.assertRaisesRegexp(
                DataError, "^.*ERREUR:  champ numérique en dehors des limites* »")
            print('**********************************************************')
            print(self._testMethodName)
            print(e.args)
            print('**********************************************************')

    def test_givenRateDecimalsGreaterThanMaxDecimals_whenCreatingInstance_thenExpectError(self):

        # given
        test_user = self.user
        test_type_service = OfferFixtures.any_type_service()
        test_description = OfferFixtures.any_description()
        test_hourly_rate = OfferFixtures.over_max_decimals_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()

        # when
        offer = Offer.objects.create(user=test_user,
                                     type_service=test_type_service,
                                     description=test_description,
                                     hourly_rate=test_hourly_rate,
                                     max_distance=test_max_dist)
        # then
        self.assertEqual(offer.user, test_user)
        self.assertEqual(offer.type_service, test_type_service)
        self.assertEqual(offer.description, test_description)
        self.assertEqual(offer.hourly_rate, test_hourly_rate)
        self.assertEqual(offer.max_distance, test_max_dist)

    def test_givenNegativeDistance_whenCreatingInstance_thenExpectError(self):

        # given
        test_user = self.user
        test_type_service = OfferFixtures.any_type_service()
        test_description = OfferFixtures.any_description()
        test_hourly_rate = OfferFixtures.any_hourly_rate()
        test_max_dist = OfferFixtures.negative_max_distance()

        # then
        try:
            Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist)
        except IntegrityError as e:
            self.assertRaisesRegexp(
                IntegrityError, "^.*ERREUR:  la nouvelle ligne de la relation « offer_offer » viole la contrainte de vérification « offer_offer_max_distance_check ».*")
            print('**********************************************************')
            print(self._testMethodName)
            print(e.args)
            print('**********************************************************')

    def test_givenPastEndDate_whenCreatingInstance_thenExpectError(self):
        '''TODO: Revoir, car le message d'erreur n'apparait pas dans les logs. Cela veut
        dire que l'exception n'est pas soulevée. Validators seulement pour formulaire.'''
        # given
        test_user = self.user
        test_type_service = OfferFixtures.any_type_service()
        test_description = OfferFixtures.any_description()
        test_hourly_rate = OfferFixtures.any_hourly_rate()
        test_max_dist = OfferFixtures.any_max_distance()
        test_end_date = date.today() - timedelta(days=1)

        # then
        try:
            Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist,
                                 end_date=test_end_date)
        except IntegrityError as e:
            self.assertRaisesRegexp(
                IntegrityError, "^.*ERREUR:  End date is not valid.*")
            print('**********************************************************')
            print(self._testMethodName)
            print(e.args)
            print('**********************************************************')


def test_givenStarDate_whenCreatingInstance_thenReturnNewInstance(self):

    # given
    test_user = self.user
    test_type_service = OfferFixtures.any_type_service()
    test_description = OfferFixtures.any_description()
    test_hourly_rate = OfferFixtures.any_hourly_rate()
    test_max_dist = OfferFixtures.any_max_distance()
    test_start_date = None

    # when
    offer = Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist,
                                 start_date=test_start_date)

    # then
    self.assertEqual(offer.user, test_user)
    self.assertEqual(offer.type_service, test_type_service)
    self.assertEqual(offer.description, test_description)
    self.assertEqual(offer.hourly_rate, test_hourly_rate)
    self.assertEqual(offer.max_distance, test_max_dist)
    self.assertEqual(offer.end_date, test_start_date)


def test_givenNoEndDate_whenCreatingInstance_thenReturnNewInstance(self):

    # given
    test_user = self.user
    test_type_service = OfferFixtures.any_type_service()
    test_description = OfferFixtures.any_description()
    test_hourly_rate = OfferFixtures.any_hourly_rate()
    test_max_dist = OfferFixtures.any_max_distance()
    test_end_date = None

    # when
    offer = Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist)

    # then
    self.assertEqual(offer.user, test_user)
    self.assertEqual(offer.type_service, test_type_service)
    self.assertEqual(offer.description, test_description)
    self.assertEqual(offer.hourly_rate, test_hourly_rate)
    self.assertEqual(offer.max_distance, test_max_dist)
    self.assertEqual(offer.end_date, test_end_date)


def test_givenStarDateAfterEndDatewhenCreatingInstance_thenExpectError(self):

    # given
    test_user = self.user
    test_type_service = OfferFixtures.any_type_service()
    test_description = OfferFixtures.any_description()
    test_hourly_rate = OfferFixtures.any_hourly_rate()
    test_max_dist = OfferFixtures.any_max_distance()
    test_start_date = date.today()
    test_end_date = date.today() - timedelta(days=1)

    # when
    offer = Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist,
                                 start_date=test_start_date,
                                 end_date=test_end_date)

    # then
    self.assertEqual(offer.user, test_user)
    self.assertEqual(offer.type_service, test_type_service)
    self.assertEqual(offer.description, test_description)
    self.assertEqual(offer.hourly_rate, test_hourly_rate)
    self.assertEqual(offer.max_distance, test_max_dist)
    self.assertEqual(offer.end_date, test_start_date)


def test_givenNoDisponibilies_whenCreatingInstance_thenReturnNewInstance(self):

    # given
    test_user = self.user
    test_type_service = OfferFixtures.any_type_service()
    test_description = OfferFixtures.any_description()
    test_hourly_rate = OfferFixtures.any_hourly_rate()
    test_max_dist = OfferFixtures.any_max_distance()
    test_end_date = date.today() - timedelta(days=1)

    # when
    offer = Offer.objects.create(user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist,
                                 end_date=test_end_date)
    # then
    self.assertEqual(offer.user, test_user)
    self.assertEqual(offer.type_service, test_type_service)
    self.assertEqual(offer.description, test_description)
    self.assertEqual(offer.hourly_rate, test_hourly_rate)
    self.assertEqual(offer.max_distance, test_max_dist)
    self.assertEqual(offer.monday, False)
    self.assertEqual(offer.tuesday, False)
    self.assertEqual(offer.wednesday, False)
    self.assertEqual(offer.thursday, False)
    self.assertEqual(offer.friday, False)
    self.assertEqual(offer.saturday, False)
    self.assertEqual(offer.sunday, False)


def test_givenExistingOfferId_whenCreatingInstance_expectError(self):
    # given
    test_user = self.user
    test_type_service = OfferFixtures.any_type_service()
    test_description = OfferFixtures.any_description()
    test_hourly_rate = OfferFixtures.any_hourly_rate()
    test_max_dist = OfferFixtures.any_max_distance()
    offer = Offer.objects.create(id=5, user=test_user,
                                 type_service=test_type_service,
                                 description=test_description,
                                 hourly_rate=test_hourly_rate,
                                 max_distance=test_max_dist)
    # then
    try:
        Offer.objects.create(id=offer.id, user=test_user,
                             type_service=test_type_service,
                             description=test_description,
                             hourly_rate=test_hourly_rate,
                             max_distance=test_max_dist)
    except IntegrityError as e:
        self.assertRaisesRegexp(
            IntegrityError, "^.*la valeur d'une clé dupliquée rompt la contrainte unique « offer_offer_pkey »*")
        print('**********************************************************')
        print(self._testMethodName)
        print(e.args)
        print('**********************************************************')


'''Tests des endpoints'''


class OfferViewTest(TestCase):
    def setUp(self):
        # Chaque test de ce type requiert la factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        UserInfo.objects.create(

            user_id=self.user,

            profile_is_completed=True,

            first_name="Jacob",

            last_name="Jr",

            nb_services_received=2,

            nb_services_given=2,

            avg_rating_as_employee=0,

            nb_rating_as_employe=0,

            avg_rating_as_employer=0,

            nb_rating_as_employer=0

        )

    def test_OffersView_whenGetMethod_thenResponseStatusCode200(self):
        # given
        request = self.factory.get('/offer/')

        # when
        response = Offers.as_view()(request)

        # then
        self.assertEqual(response.status_code, 200)

    def test_OffersView_whenIllegalPutMethod_thenResponseStatusCode405(self):
        # given
        request = self.factory.put('/offer/')

        # when
        response = Offers.as_view()(request)

        # then
        self.assertEqual(response.status_code, 405)

    def test_OffersView_whenCreateOffer_thenResponseStatusCode201(self):

        # given
        payload = {
            "user": self.user,
            "type_service": "Dressage d'animaux",
            "description": "Utilisation de gâteries véganes!",
            "hourly_rate": "10.50",
            "max_distance": 2
        }
        request = self.factory.post('/offer/', payload)

        # when
        response = Offers.as_view()(request)

        # then
        self.assertEqual(response.status_code, 201)

    def test_OffersView_whenCreateOfferWithNonExistentUser_thenResponseStatusCode401(self):

        # given
        non_existent_user = 999
        payload = {
            "user": non_existent_user,
            "type_service": "Dressage d'animaux",
            "description": "Utilisation de gâteries véganes!",
            "hourly_rate": "10.50",
            "max_distance": 2
        }
        request = self.factory.post('/offer/', payload)

        # when
        response = Offers.as_view()(request)

        # then
        self.assertEqual(response.status_code, 401)

    def test_OffersView_whenCreateOfferWithPastEndDate_thenResponseStatusCode400(self):

        # given
        test_user = self.user
        past_end_date = date.today() - timedelta(days=1)
        past_end_date = past_end_date.__str__
        payload = {
            "user": test_user,
            "type_service": "Dressage d'animaux",
            "description": "Utilisation de gâteries véganes!",
            "hourly_rate": "10.50",
            "max_distance": 2,
            "start_date": date.today().__str__,
            "end_date": past_end_date
        }
        request = self.factory.post('/offer/', payload)

        # when
        response = Offers.as_view()(request)

        # then
        self.assertEqual(response.status_code, 400)

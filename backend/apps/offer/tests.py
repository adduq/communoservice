import unittest
from django.test import RequestFactory, TestCase
from rest_framework.authtoken.models import Token
from django.core.exceptions import *
from django.db.utils import IntegrityError
from django.db import DataError
from django.contrib.auth.models import User
from apps.userinfo.models import UserInfo
from .models import Offer, ActiveOffer
from .fixtures import OfferFixtures
from .views import Offers
from datetime import date, timedelta
from pprint import pprint
from django.urls import reverse 



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
                IntegrityError, "^.*ERREUR:  End date date is not valid.*")
            print('**********************************************************')
            print(self._testMethodName)
            print(e.args)
            print('**********************************************************')


    def test_givenStartDate_whenCreatingInstance_thenReturnNewInstance(self):

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


    def test_givenStartDateAfterEndDatewhenCreatingInstance_thenExpectError(self):

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


    def test_givenNoDisponibilities_whenCreatingInstance_thenReturnNewInstance(self):

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
        
        # Measurement line
        #   from: 46.848205, -71.138826
        #   to  : 47.021290, -70.804165

        # RECRUITER DATASET
        self.recruiter = User.objects.create(
            username='gandalf',
            email='gandalf@globetrotter.net'
        )
        self.recruiter.set_password('qwerty1234')
        self.recruiter.save()
        self.recruiter_userInfo = UserInfo.objects.create(
            user_id=self.recruiter,
            first_name='Gandalf',
            last_name='LeBlanc',
            profile_is_completed= True,
            email='gandalf@globetrotter.net',
            location_lat='46.848193',
            location_lon='-71.138846',
            address='837 Rte Prévost, Saint-Pierre, QC',
        )

        # EMPLOYES DATASET

        # Region Andrew
        self.employe_andrew = User.objects.create(
            username='andrew',
            email='andrew@globetrotter.net'
        )
        self.employe_andrew.set_password('qwerty1234')
        self.employe_andrew.save()

        # Distance de l'employeur à vol d'oiseau: 1.57 km
        self.employe_andrew_userInfo = UserInfo.objects.create(
            user_id=self.employe_andrew,
            first_name='Andrew',
            last_name='Communo',
            email='andrew@globetrotter.net',
            location_lat='46.856773',
            location_lon='-71.122421',
            address='17 Rue d\'Orléans, Sainte-Pétronille, QC',
        )
        self.employe_andrew_offer = Offer.objects.create(
            user = self.employe_andrew,
            type_service = 'Administration',
            description = 'Bon service d\'administration.',
            hourly_rate = 15,
            max_distance = 4,
            date_added = '2021-11-16',
            monday = True,
            tuesday = True,
            wednesday = False,
            thursday = False,
            friday = True,
            saturday = False,
            sunday = True,
            end_date = '2021-12-30'
        )
        ActiveOffer.objects.create(
            id_offer = self.employe_andrew_offer,
            id_user = self.employe_andrew
        )

        # End region Andrew

        # Region Danic
        self.employe_danic = User.objects.create(
            username='danic',
            email='danic@globetrotter.net'
        )
        self.employe_danic.set_password('qwerty1234')
        self.employe_danic.save()

        # Distance de l'employeur à vol d'oiseau: 4.35 km
        self.employe_danic_userInfo = UserInfo.objects.create(
            user_id=self.employe_danic,
            first_name='Danic',
            last_name='Communo',
            email='danic@globetrotter.net',
            location_lat='46.871947',
            location_lon='-71.093098',
            address='933 Rte Prévost, Saint-Pierre, QC',
        )
        self.employe_danic_offer = Offer.objects.create(
            user = self.employe_danic,
            type_service = 'Déneigement',
            description = 'Bon service de déneigement.',
            hourly_rate = 15,
            max_distance = 3,
            date_added = '2021-11-16',
            monday = True,
            tuesday = False,
            wednesday = True,
            thursday = False,
            friday = True,
            saturday = True,
            sunday = True,
            end_date = '2021-12-30'
        )
        ActiveOffer.objects.create(
            id_offer = self.employe_danic_offer,
            id_user = self.employe_danic
        )
        # End region Danic

        # Region Daisy
        self.employe_daisy = User.objects.create(
            username='daisy',
            email='daisy@globetrotter.net'
        )
        self.employe_daisy.set_password('qwerty1234')
        self.employe_daisy.save()

        # Distance de l'employeur à vol d'oiseau: 6.85 km
        self.employe_daisy_userInfo = UserInfo.objects.create(
            user_id=self.employe_daisy,
            first_name='Daisy',
            last_name='Communo',
            email='daisy@globetrotter.net',
            location_lat='46.885554',
            location_lon='-71.066911',
            address='576 Rte des Prêtres, Saint-Pierre, QC',
        )
        self.employe_daisy_offer = Offer.objects.create(
            user = self.employe_daisy,
            type_service = 'Tonte de pelouse',
            description = 'Bon service de tondeuse.',
            hourly_rate = 15,
            max_distance = 15,
            date_added = '2021-11-16',
            monday = True,
            tuesday = True,
            wednesday = True,
            thursday = False,
            friday = True,
            saturday = False,
            sunday = True,
            end_date = '2021-12-30'
        )
        ActiveOffer.objects.create(
            id_offer = self.employe_daisy_offer,
            id_user = self.employe_daisy
        )
        # End region Daisy

        # Region Pierrick
        self.employe_pierrick = User.objects.create(
            username='pierrick',
            email='pierrick@globetrotter.net'
        )
        self.employe_pierrick.set_password('qwerty1234')
        self.employe_pierrick.save()

        # Distance de l'employeur à vol d'oiseau: 19.37 km
        self.employe_pierrick_userInfo = UserInfo.objects.create(
            user_id=self.employe_pierrick,
            first_name='Pierrick',
            last_name='Communo',
            email='pierrick@globetrotter.net',
            location_lat='46.954251',
            location_lon='-70.936578',
            address='1099 Rte du Mitan, Sainte-Famille, QC',
        )
        self.employe_pierrick_offer = Offer.objects.create(
            user = self.employe_pierrick,
            type_service = 'Gardiennage',
            description = 'Bon service de gardiennage.',
            hourly_rate = 15,
            max_distance = 10,
            date_added = '2021-11-16',
            monday = False,
            tuesday = False,
            wednesday = True,
            thursday = True,
            friday = True,
            saturday = False,
            sunday = False,
            end_date = '2021-12-30'
        )
        ActiveOffer.objects.create(
            id_offer = self.employe_pierrick_offer,
            id_user = self.employe_pierrick
        )
        # End region Pierrick

    def test_OffersView_whenGetAllActiveOffersWithoutToken_thenNoDistanceCalculated(self):
        response = self.client.get(reverse('active-offers'))
        offers = [dict(obj) for obj in response.data]
        self.assertEqual(len(offers), 4)

    def test_OffersView_whenGetAllActiveOffersWithToken_thenDistanceCalculated(self):
        # Devrait contenir le service de andrew (Administration)
        # Ne devrait pas contenir le service de Danic (Déneigement)
        # Devrait contenir le service de Daisy (Tonte de pelouse)
        # Ne devrait pas contenir le service de Pierrick (Gardiennage)

        login_data = {
            'username': self.recruiter.username,
            'password': 'qwerty1234',
        }

        response = self.client.post(reverse('login'), login_data, format='json')
        token = response.data['auth_token']

        headers = {
           'HTTP_AUTHORIZATION': 'Token  ' + token
        }
        response = self.client.get(reverse('active-offers'), **headers)
        offers = [dict(obj) for obj in response.data]

        self.assertTrue(any("Administration" in offer['type_service'] for offer in offers))
        self.assertTrue(any("Tonte de pelouse" in offer['type_service'] for offer in offers))
        self.assertFalse(any("Déneigement" in offer['type_service'] for offer in offers))
        self.assertFalse(any("Gardiennage" in offer['type_service'] for offer in offers))
        self.assertEqual(len(offers), 2)

    def test_OffersView_whenLoginAsRecruiter_thenAuthTokenReturned(self):
        login_data = {
            'username': self.recruiter.username,
            'password': 'qwerty1234',
        }
        response = self.client.post(reverse('login'), data=login_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.data)

        token = Token.objects.get(user=self.recruiter)
        self.assertEqual(response.data['auth_token'], token.key)

        # TODO: Utiliser API Client => https://stackoverflow.com/questions/29140353/testing-django-api-login-using-credentials-and-djoser

    def test_OffersView_whenGetMethodOnOffers_thenResponseStatusCode200(self):
        # when
        response = self.client.get(reverse('offers'))
        # then
        self.assertEqual(response.status_code, 200)

    def test_OffersView_whenGettingOfferById_thenResponseStatusCode200(self):
        created_offer = Offer.objects.create(
            user = self.recruiter,
            type_service = 'Gardiennage',
            description = 'Bon service de gardiennage.',
            hourly_rate = 15,
            max_distance = 10,
            date_added = '2021-11-16',
            monday = False,
            tuesday = False,
            wednesday = True,
            thursday = True,
            friday = True,
            saturday = False,
            sunday = False,
            end_date = '2021-12-30'
        )
        created_offer.save()

        active_offer = ActiveOffer.objects.create(
            id_user = self.recruiter,
            id_offer = created_offer
        )
        active_offer.save()
        # when
        response = self.client.get(reverse('active-offers', kwargs={'id_active_offer': created_offer.id}))
        
        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], created_offer.id)
        created_offer.delete()

    def test_OffersView_whenIllegalPutMethod_thenResponseStatusCode405(self):
        # when
        response = self.client.put(reverse('offers'))
        # then
        self.assertEqual(response.status_code, 405)

    def test_OffersView_whenCreateOfferWithoutToken_thenResponseStatusCode401(self):
        # given
        payload = {
            "user" : self.recruiter.id,
            "type_service" : 'Tonte de pelouse',
            "description" : 'Service de tonte de pelouse.',
            "hourly_rate" : 15,
            "max_distance" : 10,
            "date_added" : '2021-11-16',
            "monday" : False,
            "tuesday" : False,
            "wednesday" : True,
            "thursday" : True,
            "friday" : True,
            "saturday" : False,
            "sunday" : False,
            "end_date" : '2021-12-30'
        }
        #when
        response = self.client.post(reverse('offers'), data=payload)

        # then
        self.assertEqual(response.status_code, 401)

    def test_OffersView_whenCreateOfferWithNonExistentUser_thenResponseStatusCode403(self):
        # given
        login_data = {
            'username': self.recruiter.username,
            'password': 'qwerty1234',
        }

        response = self.client.post(reverse('login'), data=login_data, format='json')
        token = response.data['auth_token']

        headers = {
           'HTTP_AUTHORIZATION': 'Token  ' + token
        }

        non_existent_user = 999
        payload = {
            "user": non_existent_user,
            "type_service" : 'Tonte de pelouse',
            "description" : 'Service de tonte de pelouse.',
            "hourly_rate" : 15,
            "max_distance" : 10,
            "date_added" : '2021-11-16',
            "monday" : False,
            "tuesday" : False,
            "wednesday" : True,
            "thursday" : True,
            "friday" : True,
            "saturday" : False,
            "sunday" : False,
            "end_date" : '2021-12-30'
        }
        # when
        response = self.client.post(reverse('offers'), data=payload, **headers)
       
        # then
        self.assertEqual(response.status_code, 403)

    def test_OffersView_whenCreateOfferWithPastEndDate_thenResponseStatusCode400(self):

        # given
        login_data = {
            'username': self.recruiter.username,
            'password': 'qwerty1234',
        }

        response = self.client.post(reverse('login'), data=login_data, format='json')
        token = response.data['auth_token']

        headers = {
           'HTTP_AUTHORIZATION': 'Token  ' + token
        }

        past_end_date = date.today() - timedelta(days=1)
        past_end_date = past_end_date.__str__
        payload = {
            "user": self.recruiter,
            "type_service" : 'Tonte de pelouse',
            "description" : 'Service de tonte de pelouse.',
            "hourly_rate" : 15,
            "max_distance" : 10,
            "date_added" : '2021-11-16',
            "monday" : False,
            "tuesday" : False,
            "wednesday" : True,
            "thursday" : True,
            "friday" : True,
            "saturday" : False,
            "sunday" : False,
            "end_date": past_end_date
        }
        # when
        response = self.client.post(reverse('offers'), data=payload, **headers)

        # then
        self.assertEqual(response.status_code, 400)
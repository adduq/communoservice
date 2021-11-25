import unittest
from django.test import RequestFactory, TestCase

from django.core.exceptions import *
from django.db.utils import IntegrityError
from django.db import DataError
from django.contrib.auth.models import User
from .models import UserInfo
#from .fixtures import OfferFixtures
from django.urls import reverse 
from pprint import pprint


'''https://www.geeksforgeeks.org/python-assertion-error/'''

'''Tests du model UserInfo'''

# Tester le trigger dans la BD

class TestUserInfo(TestCase):
    def setUp(self):
         # RECRUITER DATASET
        self.aragorn = User.objects.create(
            username='aragorn',
            email='aragorn@globetrotter.net'
        )
        self.aragorn.set_password('qwerty1234')
        self.aragorn.save()
        self.aragorn_userinfo = UserInfo.objects.create(
            user_id=self.aragorn,
            first_name='Aragorn',
            last_name='LeBlanc',
            profile_is_completed= True,
            email='aragorn@globetrotter.net',
            location_lat='46.848193',
            location_lon='-71.138846',
            address='837 Rte Prévost, Saint-Pierre, QC',
        )
    
    def tearDown(self):
        self.aragorn.delete()
    
    def test_UserInfoDetail_whenGetUserInfoAsOtherUser_thenCorrectInfoReturned(self):
        login_data = {
            'username': self.aragorn.username,
            'password': 'qwerty1234',
        }

        response = self.client.post(reverse('login'), login_data, format='json')
        token = response.data['auth_token']

        headers = {
           'HTTP_AUTHORIZATION': 'Token  ' + token
        }
        response = self.client.get(reverse('userinfo', kwargs={'user_id': self.aragorn.id}), **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('first_name' in response.data and response.data['first_name'] == self.aragorn_userinfo.first_name)
        self.assertTrue('last_name' in response.data and response.data['last_name'] == self.aragorn_userinfo.last_name)
        self.assertTrue('user_id' in response.data and response.data['user_id'] == self.aragorn_userinfo.user_id.id)
        self.assertFalse('id' in response.data)
        self.assertFalse('profile_is_completed' in response.data)
        self.assertFalse('email' in response.data)
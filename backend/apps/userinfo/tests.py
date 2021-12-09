from django.test import TestCase
from django.core.exceptions import *
from django.contrib.auth.models import User
from .models import UserInfo
from django.urls import reverse 
import json

'''Tests du model UserInfo'''
class TestUserInfo(TestCase):
    def setUp(self):
        # RECRUITER DATASET
        self.recruiter = User.objects.create(
            username='gandalf',
            email='gandalf@globetrotter.net'
        )
        self.recruiter.set_password('qwerty1234')
        self.recruiter.save()
        self.recruiter_userinfo = UserInfo.objects.create(
            user_id=self.recruiter,
            first_name='Gandalf',
            last_name='LeBlanc',
            profile_is_completed= True,
            email='gandalf@globetrotter.net',
            location_lat='46.848193',
            location_lon='-71.138846',
            user_bio='Biographie compliquée.',
            address='837 Rte Prévost, Saint-Pierre, QC',
        )
        # EMPLOYEE DATASET
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
            user_bio='Biographie simple.',
            address='837 Rte Prévost, Saint-Pierre, QC',
        )
        self.login()
    
    def login(self):
        login_data = {
            'username': self.aragorn.username,
            'password': 'qwerty1234',
        }

        response = self.client.post(reverse('login'), login_data, format='json')
        token = response.data['auth_token']

        self.headers = {
           'HTTP_AUTHORIZATION': 'Token  ' + token
        }

    def tearDown(self):
        self.aragorn.delete()
    
    def test_UserInfoDetail_whenGetExistingUserInfoAsOtherUser_thenCorrectInfoReturned(self):
        response = self.client.get(reverse('userinfo', kwargs={'user_id': self.aragorn.id}), **self.headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('first_name' in response.data and response.data['first_name'] == self.aragorn_userinfo.first_name)
        self.assertTrue('last_name' in response.data and response.data['last_name'] == self.aragorn_userinfo.last_name)
        self.assertTrue('user_id' in response.data and response.data['user_id'] == self.aragorn_userinfo.user_id.id)
        self.assertFalse('id' in response.data)
        self.assertFalse('profile_is_completed' in response.data)
        self.assertFalse('email' in response.data)
    
    def test_UserInfoDetail_whenGetNonExistentUserInfoAsOtherUser_thenStatusCode404(self):
        response = self.client.get(reverse('userinfo', kwargs={'user_id': 999}), **self.headers)
        
        self.assertEqual(response.status_code, 404)

    def test_MyUserInfo_whenGetSelfUserInfo_thenCorrectInfoReturned(self):
        response = self.client.get(reverse('userinfo/me/'), **self.headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue('first_name' in response.data and response.data['first_name'] == self.aragorn_userinfo.first_name)
        self.assertTrue('last_name' in response.data and response.data['last_name'] == self.aragorn_userinfo.last_name)
        self.assertTrue('user_id' in response.data and response.data['user_id'] == self.aragorn_userinfo.user_id.id)

    def test_UpdateUserInfo_whenChangingUserInfo_thenInformationSaved(self):
        updatedUserInfo = {
            "user_bio": "Test biographie"
        }
        response = self.client.put(reverse('userinfo/me/update/'), data=json.dumps(updatedUserInfo), content_type="application/json", **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user_bio' in response.data and response.data['user_bio'] == updatedUserInfo['user_bio'])

    def test_UserStatus_whenValidToken_thenStatusCode200(self):
        response = self.client.get(reverse('userinfo/me/status/'), **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_UserStatus_whenInvalidToken_thenStatusCode401(self):
        invalidHeaders = {
            'HTTP_AUTHORIZATION': 'Token  133713371337133713371337'
        }
        response = self.client.get(reverse('userinfo/me/status/'), **invalidHeaders)
        self.assertEqual(response.status_code, 401)
    
    def test_UpdateEmployeeRating_whenUpdatingEmployeeRatingWithHigherScore_thenScoreIsHigher(self):
        login_data = {
            'username': self.recruiter.username,
            'password': 'qwerty1234',
        }

        response = self.client.post(reverse('login'), data=login_data, format='json')
        token = response.data['auth_token']
        headers = {
           'HTTP_AUTHORIZATION': 'Token  ' + token
        }

        new_rating = {
            "rating" : "5"
        }
        response = self.client.put(reverse('userinfo/<user_id>/update-employee/<recruiter_id>/', kwargs={"user_id": self.aragorn.id, "recruiter_id": self.recruiter.id}), data=json.dumps(new_rating), content_type="application/json", **headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('avg_rating_as_employee' in response.data and float(response.data['avg_rating_as_employee']) > 0)

        #TODO: TEST STATUS CODES 401 & 403
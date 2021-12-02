import os
from django.http import Http404, HttpResponse, JsonResponse
from django.conf import settings
from PIL import Image, ImageOps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view  # Pour utilser annotations
from django.contrib.auth.models import User

from rest_framework import status
from .models import UserInfo
from .serializers import UserInfoSerializer, UserSerializer

from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema
from django.core.validators import validate_email

import re, json


from pprint import pprint
# Create your views here.


class UserInfoDetail(APIView):

    """
    Récupérer l'info d'un utilisateur à l'aide de son identifiant.
    """

    def get_object(self, user_id):
        try:

            user = UserInfo.objects.get(user_id=user_id)

            auth_user = User.objects.get(id=user_id)
            serializer = UserInfoSerializer(user)

            out_dict = {'is_active':auth_user.is_active, 'username':auth_user.username}
            out_dict.update(serializer.data)

            del out_dict['id']
            del out_dict['email']
            del out_dict['profile_is_completed']

            return out_dict
        except UserInfo.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        userinfo = self.get_object(user_id)
        return Response(userinfo)

class MyUserInfo(APIView):

    """
    Récupérer l'info de l'utilisateur à l'aide de son token.
    """

    def get_object(self, user_id):
        try:

            user = UserInfo.objects.get(user_id=user_id)
            serializer = UserInfoSerializer(user)
            auth_user = User.objects.get(id=user_id)

            out_dict = {'is_active':auth_user.is_active, 'username':auth_user.username}
            out_dict.update(serializer.data)
            
            del out_dict['id']

            return out_dict
        except UserInfo.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

        userinfo = self.get_object(request.user.id)
        return Response(userinfo)

class UpdateUserInfo(APIView):

    """
    Modifier l'info de l'utilisateur actif à l'aide de son token.
    """

    def put(self, request, format=None):

        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

        try:
            user = UserInfo.objects.get(user_id=request.user.id)
            userObject = User.objects.get(id=request.user.id)

            body = json.loads(request.body)

            if 'first_name' in body:
                if body['first_name'] == '' or re.match(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð-]{2,15}$", body['first_name']):
                    user.first_name = body['first_name']
                    userObject.first_name = body['first_name']
                else:
                    return Response('Le prénom est invalide.', status=status.HTTP_400_BAD_REQUEST)

            if 'last_name' in body:
                if body['last_name'] == '' or re.match(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð-]{2,15}$", body['last_name']):
                    user.last_name = body['last_name']
                    userObject.last_name = body['last_name']
                else:
                    return Response('Le nom est invalide.', status=status.HTTP_400_BAD_REQUEST)

            if 'email' in body:
                if body['email'] == '' or re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", body['email']):
                    user.email = body['email']
                    userObject.email = body['email']
                else:
                    return Response('Le courriel est invalide.', status=status.HTTP_400_BAD_REQUEST)

            if 'address' in body:
                if len(body['address']) < 100:
                    user.address = body['address']
                else:
                    return Response('L\'adresse est invalide.', status=status.HTTP_400_BAD_REQUEST)

            if 'user_bio' in body:
                user.user_bio = body['user_bio']
            
            if 'location_lat' in body:
                user.location_lat = body['location_lat']
            
            if 'location_lon' in body:
                user.location_lon = body['location_lon']

            if user.first_name != '' and user.first_name != None and \
                user.last_name != '' and user.last_name != None and \
                user.email != '' and user.email != None and \
                user.address != '' and user.address != None and\
                user.location_lat != '' and user.location_lat != None and\
                user.location_lon != '' and user.location_lon != None:

                user.profile_is_completed = True
            else:
                user.profile_is_completed = False

            user.save()
            userObject.save()

            serializer = UserInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserInfo.DoesNotExist:
            raise Http404

class UserStatus(APIView):
    """
    Permet de valider l'état du token de l'utilisateur.
    """

    def get(self, request, format=None):
        if request.user.is_anonymous:
            return Response({"status":"invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"status":"valid"}, status=status.HTTP_200_OK)
        

class UpdateEmployeeRating(APIView):

    def put(self, request, user_id, recruiter_id, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if (recruiter_id is not None and request.user.id != recruiter_id):
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
        # if ((recruiter_id is not None and request.user.id != recruiter_id) and
        #         (user_id is not None and request.user.id != user_id)):
        #     return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        userinfo = UserInfo.objects.get(user_id=user_id)

        if 'rating' in request.data and request.data['rating'] is not None and float(request.data['rating']) >= 0 and float(request.data['rating']) <= 5:
            userinfo.avg_rating_as_employee = (((float(userinfo.avg_rating_as_employee) * userinfo.nb_rating_as_employe)
                                                + float(request.data['rating'])) / (userinfo.nb_rating_as_employe + 1))
            userinfo.nb_rating_as_employe += 1
            userinfo.nb_services_given += 1

            userinfo.save()
        
        serializer = UserInfoSerializer(userinfo)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateRecruiterRating(APIView):

    def put(self, request, user_id, recruiter_id, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if (user_id is not None and request.user.id != user_id):
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)
        # if ((recruiter_id is not None and request.user.id != recruiter_id) and
        #         (user_id is not None and request.user.id != user_id)):
        #     return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        userinfo = UserInfo.objects.get(user_id=recruiter_id)

        if 'rating' in request.data and request.data['rating'] is not None and float(request.data['rating']) >= 0 and float(request.data['rating']) <= 5:
            userinfo.avg_rating_as_employer = (((float(userinfo.avg_rating_as_employer) * userinfo.nb_rating_as_employer)
                                                + float(request.data['rating'])) / (userinfo.nb_rating_as_employer + 1))
            userinfo.nb_rating_as_employer += 1
            userinfo.nb_services_received += 1

            userinfo.save()
        
        serializer = UserInfoSerializer(userinfo)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUserProfileImage(APIView):
    def post(self, request):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.FILES['image']:
                im = Image.open(request.FILES['image'])
                rgb_im = im.convert('RGB')

                size_300 = (300, 300)

                thumb_300 = ImageOps.fit(rgb_im, size_300, Image.ANTIALIAS)

                thumb_300.save(str(settings.MEDIA_ROOT)+ '/' + 'pfp_' + str(request.user.id) + '.jpg')
                return Response({"status": "Added successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "No files in request"}, status=status.HTTP_400_BAD_REQUEST)


class GetUserImage(APIView):
    def get(self, request, user_id, format=None):
        # if request.user.is_anonymous:
        #     return Response({"status": "invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        imgExist = os.path.exists(
            str(settings.MEDIA_ROOT) + '/' + 'pfp_' + str(user_id) + '.jpg')
        imgName = 'pfp_default.jpg'

        if (imgExist):
            imgName = 'pfp_' + str(user_id) + '.jpg'

        return Response({"imgName": imgName}, status=status.HTTP_200_OK)

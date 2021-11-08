from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.forms.models import model_to_dict

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
            body = json.loads(request.body)

            if 'first_name' in body:
                if body['first_name'] == '' or re.match(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð-]{2,15}$", body['first_name']):
                    user.first_name = body['first_name']
                else:
                    return Response('Le prénom est invalide.', status=status.HTTP_400_BAD_REQUEST)

            if 'last_name' in body:
                if body['last_name'] == '' or re.match(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð-]{2,15}$", body['last_name']):
                    user.last_name = body['last_name']
                else:
                    return Response('Le nom est invalide.', status=status.HTTP_400_BAD_REQUEST)

            if 'email' in body:
                if body['email'] == '' or re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", body['email']):
                    user.email = body['email']
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
            serializer = UserInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except UserInfo.DoesNotExist:
            raise Http404

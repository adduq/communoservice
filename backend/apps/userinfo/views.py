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

# Create your views here.


class UserInfoDetail(APIView):

    """
    Récupérer l'info d'un utilisateur à l'aide de son identifiant.
    """

    def get_object(self, user):
        try:

            user = UserInfo.objects.get(user=user)

            user_is_active = User.objects.get(id=user).is_active
            serializer = UserInfoSerializer(user)

            out_dict = {'is_active':user_is_active}
            out_dict.update(serializer.data)

            del out_dict['id']
            del out_dict['email']
            del out_dict['profile_is_completed']

            return out_dict
        except UserInfo.DoesNotExist:
            raise Http404

    def get(self, request, user, format=None):
        userinfo = self.get_object(user)
        return Response(userinfo)

class MyUserInfo(APIView):

    """
    Récupérer l'info de l'utilisateur à l'aide de son token.
    """

    def get_object(self, user):
        try:

            userinfo = UserInfo.objects.get(user=user)
            serializer = UserInfoSerializer(userinfo)
            user_is_active = User.objects.get(id=user.id).is_active

            out_dict = {}
            out_dict.update(serializer.data)
            
            del out_dict['id']
            del out_dict['email']
            return out_dict
        except UserInfo.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        if request.user.is_anonymous:
            return HttpResponse('Unauthorized', status=401)

        userinfo = self.get_object(request.user)
        return Response(userinfo)
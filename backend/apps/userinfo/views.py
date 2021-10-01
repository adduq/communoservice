from django.db.models import Q
from django.http import Http404

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
    Récupérer l'info d'un user selon l'id de du user.
    """

    def get_object(self, user_id):
        try:
            return UserInfo.objects.get(id=user_id)
        except UserInfo.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        userinfo = self.get_object(user_id)
        serializer = UserInfoSerializer(userinfo)
        return Response(serializer.data)
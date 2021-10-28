from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view  # Pour utilser annotations
from django.contrib.auth.models import User

from rest_framework import status
from .models import Offer
from .serializers import OfferSerializer

from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema

from functools import reduce
from operator import and_


class Offers(APIView):

    """
    Récupèrer toutes les offres.
    """

    def get(self, request, format=None):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    """
    Création d'une offre.
    """

    def post(self, request, format=None):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferDetail(APIView):

    """
    Récupérer une offre selon l'id de l'offre.
    """

    def get_object(self, no_offer):
        try:
            return Offer.objects.get(id=no_offer)
        except Offer.DoesNotExist:
            raise Http404

    def get(self, request, no_offer, format=None):
        offer = self.get_object(no_offer)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)


class UserOffers(APIView):
    """
    Récupérer toutes les offres d'un employé.
    """

    def get_object(self, no_user):
        try:
            return Offer.objects.filter(user=no_user)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, no_user, format=None):
        offer = self.get_object(no_user)
        serializer = OfferSerializer(offer, many=True)
        return Response(serializer.data)


'''
Permet de rechercher des offres selon le type de service.
'''


@api_view(['GET'])
def search(request):
    queryset = Offer.objects.all()
    if "type-service" in request.GET:
        queryset = queryset.filter(type_service__icontains=request.GET.get('type-service'))

    if "day-of-week" in request.GET:
        date = request.GET.get('date')
        dow = request.GET.get('day-of-week')

        if dow == "monday":
            queryset = queryset.filter(monday=True)
        if dow == "tuesday":
            queryset = queryset.filter(tuesday=True)
        if dow == "thursday":
            queryset = queryset.filter(thursday=True)
        if dow == "wednesday":
            queryset = queryset.filter(wednesday=True)
        if dow == "friday":
            queryset = queryset.filter(friday=True)
        if dow == "saturday":
            queryset = queryset.filter(saturday=True)
        if dow == "sunday":
            queryset = queryset.filter(sunday=True)
        
        queryset.filter(expiration_date__gte=date)
    
    if "mots-cles" in request.GET:
        mots_cles = request.GET.getlist('mots-cles')[0].split(',')
        queryset = queryset.filter(reduce(and_, (Q(description__icontains=mot) for mot in mots_cles)))

    serializer = OfferSerializer(queryset, many=True)
    return Response(serializer.data)
from typing import OrderedDict
import requests
from django.db.models import Q
from django.http import Http404
from django.http.response import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view  # Pour utilser annotations
from django.contrib.auth.models import User

from rest_framework import status
from .models import ActiveOffer, Offer, ReservedOffer, ServiceType, TerminatedOffer
from apps.userinfo.models import UserInfo
from .serializers import ActiveOfferCreationSerializer, ActiveOfferSerializer, OfferSerializer, ReservedOfferCreationSerializer, ReservedOfferSerializer, ServiceTypeSerializer, TerminatedOfferCreationSerializer, TerminatedOfferSerializer

from rest_framework.decorators import api_view

from functools import reduce
from operator import and_
from math import cos, asin, sqrt, pi


from pprint import pprint


PUBLIC_MAPBOX_KEY = "pk.eyJ1IjoidmFuaXR5cHciLCJhIjoiY2t2a2FhcmxmZDNkOTJxcTYybXNkODRoZSJ9.dNeojMWUvXZH-TkiFqTexA"

def sort_offers_by_distance(user_id, offers):

    me = UserInfo.objects.get(user_id=user_id)

    def haversine(lat1, lon1, lat2, lon2):
        p = pi/180
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(a))

    def check_distance(offer):
        employe = UserInfo.objects.get(user_id=offer['user'])
        dist = haversine(float(me.location_lat), float(me.location_lon), float(employe.location_lat), float(employe.location_lon))        
        if dist < float(offer['max_distance']):
            return driving_distance(employe.location_lon, employe.location_lat, offer['max_distance'])
        else:
            return False
    
    def driving_distance(employe_lon, employe_lat, max_distance):
        #if driving distance > offer['max_distance'] then exclude from candidates
        formated_url = "https://api.mapbox.com/directions/v5/mapbox/driving/{0},{1};{2},{3}?access_token={4}".format(me.location_lon, me.location_lat, employe_lon, employe_lat, PUBLIC_MAPBOX_KEY)
        response = requests.get(formated_url)
        data = response.json()
        print(data)
        if data['code'] == 'NoRoute':
            return False
        else:
            print(data['routes'][0]['distance'])
            return float(data['routes'][0]['distance'])/1000 < float(max_distance)

    if me.location_lat != '' and me.location_lon != '':
        print('Sorting offers for user ' + str(user_id))
        potential_offers = map(check_distance, offers)
        return [d for (d, keep) in zip(offers, potential_offers) if keep]
    else:
        print('User not compliant for sort_offers_by_distance')
        return offers


def remove_user_infos(serializer):
    for elem in serializer.data:
        if 'id_user' in elem:
            elem['user'] = {
                'id': elem['id_user']['id'],
                'last_name': elem['id_user']['last_name'],
                'first_name': elem['id_user']['first_name'],
                'username': elem['id_user']['username'],
            }
            del elem['id_user']
            elem['id_user'] = elem['user']
            del elem['user']

        if 'id_recruiter' in elem:
            elem['recruiter'] = {
                'id': elem['id_recruiter']['id'],
                'last_name': elem['id_recruiter']['last_name'],
                'first_name': elem['id_recruiter']['first_name'],
                'username': elem['id_recruiter']['username'],
            }
            del elem['id_recruiter']
            elem['id_recruiter'] = elem['recruiter']
            del elem['recruiter']

    return serializer.data


class Offers(APIView):

    """
    Récupèrer toutes les offres.
    """

    # def get(self, request, format=None):
    #     offers = Offer.objects.all()
    #     serializer = OfferSerializer(offers, many=True)
    #     return Response(serializer.data)

    """
    Création d'une offre.
    """

    def user_can_create(self, user_id):
        user = UserInfo.objects.get(user_id=user_id)
        return user.profile_is_completed

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        # pprint(request.data)

        if request.data['user'] is not None and request.user.id != request.data['user']:
            return Response('Forbidden', status=403)

        if self.user_can_create(request.user.id):
            serializer = OfferSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {'error': 'profile_incomplete'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


# class OfferDetail(APIView):

#     """
#     Récupérer une offre selon l'id de l'offre.
#     """

#     def get_object(self, no_offer):
#         try:
#             return Offer.objects.get(id=no_offer)
#         except Offer.DoesNotExist:
#             raise Http404

#     def get(self, request, no_offer, format=None):
#         offer = self.get_object(no_offer)
#         serializer = OfferSerializer(offer)
#         return Response(serializer.data)


class ServiceTypes(APIView):
    def get(self, request, format=None):
        service_types = ServiceType.objects.all()
        serializer = ServiceTypeSerializer(service_types, many=True)
        return Response(serializer.data)

# # Note:
# # ? Utiliser activeOffer à la place ?
# class UserOffers(APIView):
#     """
#     Récupérer toutes les offres d'un employé.
#     """

#     def get_object(self, no_user):
#         try:
#             return Offer.objects.filter(user=no_user)
#         except User.DoesNotExist:
#             raise Http404

#     def get(self, request, no_user, format=None):
#         offer = self.get_object(no_user)
#         serializer = OfferSerializer(offer, many=True)
#         return Response(serializer.data)

# region ActiveOffers


class ActiveOffers(APIView):
    """
    Permet d'avoir les offres actives.
    """

    # def get_offers(self):
    #     active_offers = list(
    #         ActiveOffer.objects.all().values_list('id_offer', flat=True))
    #     return Offer.objects.filter(id__in=active_offers)

    def get(self, request, format=None):
        # active_offers = self.get_offers()
        # serializer = OfferSerializer(active_offers, many=True)

        if not request.user.is_anonymous:
            active_offers = ActiveOffer.objects.exclude(
                id_user=request.user.id)
        else:
            active_offers = ActiveOffer.objects.all()

        serializer = ActiveOfferSerializer(active_offers, many=True)

        offers = []
        remove_user_infos(serializer)
        # pprint(serializer.data)

        for elem in serializer.data:
            offers.append(elem['id_offer'])

        if not request.user.is_anonymous:            
            offers = sort_offers_by_distance(
                request.user.id, [dict(obj) for obj in offers])
            # offers = sort_offers_by_distance(request.user.id, [dict(obj) for obj in serializer.data])
        # else:
        #     # offers = serializer.data

        return Response(offers)

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        # pprint(request.data)

        if request.data['id_user'] is not None and request.user.id != request.data['id_user']:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        serializer = ActiveOfferCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveOffersByUser(APIView):
    """
    Permet d'avoir les offres actives par utilisateur.
    """
    # ? Note: Ajouter validation ici ou accessible à tous ?
    # ! TODO: Ajouter validation sur le no_user

    # def get_offers(self, no_user):
    #     active_offers = list(
    #         ActiveOffer.objects.filter(id_user=no_user).values_list('id_offer', flat=True))
    #     return Offer.objects.filter(id__in=active_offers)

    def get(self, request, no_user, format=None):
        # active_offers = self.get_offers(no_user)
        # serializer = OfferSerializer(active_offers, many=True)

        active_offers = ActiveOffer.objects.filter(id_user=no_user)
        serializer = ActiveOfferSerializer(active_offers, many=True)

        offers = []
        remove_user_infos(serializer)

        for elem in serializer.data:
            offers.append(elem['id_offer'])

        return Response(offers)


class ActiveOfferWithId(APIView):
    # ? Note: Ajouter validation ici ou accessible à tous ?

    def get(self, request, no_user, id_offer, format=None):
        offers = ActiveOffer.objects.get(id_offer=id_offer, id_user=no_user)
        serializer = ActiveOfferCreationSerializer(offers)
        return Response(serializer.data)


class ActiveOfferDetail(APIView):
    """
    Permet d'avoir ou de supprimer une offre active selon son id.
    """

    def get_object(self, id_active_offer):
        try:
            return ActiveOffer.objects.get(id=id_active_offer)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, id_active_offer, format=None):
        active_offer = self.get_object(id_active_offer)
        serializer = ActiveOfferCreationSerializer(active_offer)
        return Response(serializer.data)

    def delete(self, request, id_active_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        # pprint(request.data)
        # ? Note: Comment valider ici ?
        # if request.data['id_user'] is not None and request.user.id != request.data['id_user']:
        #     return Response('Forbidden', status=403)

        active_offer = self.get_object(id_active_offer)
        active_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# endregion

# region ReservedOffers


class ReservedOffers(APIView):
    """
    Permet d'avoir les offres réservées.
    """

    # def get(self, request, format=None):
    #     reserved_offers = ReservedOffer.objects.all()
    #     serializer = ReservedOfferSerializer(reserved_offers, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        # pprint(request.data)

        if request.data['id_recruiter'] is not None and request.user.id != request.data['id_recruiter']:
            return Response('Forbidden', status=403)

        serializer = ReservedOfferCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservedOffersByUser(APIView):
    """
    Permet d'avoir les offres réservées par utilisateur.
    """

    def get(self, request, no_user, format=None):
        if request.user.is_anonymous or request.user.id != no_user:
            return Response('Unauthorized', status=401)

        reserved_offers = ReservedOffer.objects.filter(id_user=no_user)
        serializer = ReservedOfferSerializer(reserved_offers, many=True)
        remove_user_infos(serializer)
        return Response(serializer.data)


class ReservedOffersByRecruiter(APIView):
    """
    Permet d'avoir les offres réservées en tant qu'employeur.
    """

    def get(self, request, no_recruiter, format=None):
        if request.user.is_anonymous or request.user.id != no_recruiter:
            return Response('Unauthorized', status=401)

        reserved_offers = ReservedOffer.objects.filter(
            id_recruiter=no_recruiter)
        serializer = ReservedOfferSerializer(reserved_offers, many=True)
        remove_user_infos(serializer)
        return Response(serializer.data)


class ReservedOfferDetail(APIView):
    """
    Permet d'avoir une offre réservée.
    """

    def get_object(self, id_reserved_offer):
        try:
            return ReservedOffer.objects.get(id=id_reserved_offer)
        except User.DoesNotExist:
            raise Http404

    # def get(self, request, id_reserved_offer, format=None):
    #     reserved_offer = self.get_object(id_reserved_offer)
    #     serializer = ReservedOfferSerializer(reserved_offer)
    #     return Response(serializer.data)

    def delete(self, request, id_reserved_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        reserved_offer = self.get_object(id_reserved_offer)
        reserved_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id_reserved_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        if ((request.data['id_recruiter'] is not None and request.user.id != request.data['id_recruiter']) or
            (request.data['id_user'] is not None and request.user.id != request.data['id_user'])):
            return Response('Forbidden', status=403)

        reserved_offer = self.get_object(id_reserved_offer)
        serializer = ReservedOfferCreationSerializer(
            reserved_offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion

# region TerminatedOffers


class TerminatedOffers(APIView):
    """
    Permet d'avoir les offres terminées.
    """

    # def get(self, request, format=None):
    #     terminated_offers = TerminatedOffer.objects.all()
    #     serializer = TerminatedOfferSerializer(terminated_offers, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        # pprint(request.data)

        if request.data['id_user'] is not None and request.user.id != request.data['id_user']:
            return Response('Forbidden', status=403)

        serializer = TerminatedOfferCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TerminatedOffersByUser(APIView):
    """
    Permet d'avoir les offres terminées par utilisateur.
    """

    def get(self, request, no_user, format=None):
        if request.user.is_anonymous or request.user.id != no_user:
            return Response('Unauthorized', status=401)

        terminated_offers = TerminatedOffer.objects.filter(id_user=no_user)
        serializer = TerminatedOfferSerializer(terminated_offers, many=True)
        remove_user_infos(serializer)
        return Response(serializer.data)


class TerminatedOffersByRecruiter(APIView):
    """
    Permet d'avoir les offres terminées en tant qu'employeur.
    """

    def get(self, request, no_recruiter, format=None):
        if request.user.is_anonymous or request.user.id != no_recruiter:
            return Response('Unauthorized', status=401)

        terminated_offers = TerminatedOffer.objects.filter(
            id_recruiter=no_recruiter)
        serializer = TerminatedOfferSerializer(terminated_offers, many=True)
        remove_user_infos(serializer)
        return Response(serializer.data)


class TerminatedOfferDetail(APIView):
    """
    Permet d'avoir une offre terminée.
    """

    def get_object(self, id_terminated_offer):
        try:
            return TerminatedOffer.objects.get(id=id_terminated_offer)
        except User.DoesNotExist:
            raise Http404

    # def get(self, request, id_terminated_offer, format=None):
    #     terminated_offer = self.get_object(id_terminated_offer)
    #     serializer = TerminatedOfferSerializer(terminated_offer)
    #     return Response(serializer.data)

    def delete(self, request, id_terminated_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        terminated_offer = self.get_object(id_terminated_offer)
        terminated_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id_terminated_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=401)

        if ((request.data['id_recruiter'] is not None and request.user.id != request.data['id_recruiter']) or
            (request.data['id_user'] is not None and request.user.id != request.data['id_user'])):
            return Response('Forbidden', status=403)

        terminated_offer = self.get_object(id_terminated_offer)
        serializer = TerminatedOfferCreationSerializer(
            terminated_offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# endregion


"""
Permet de rechercher des offres.
"""
@api_view(['GET'])
def search(request):
    active_offers = list(
        ActiveOffer.objects.all().values_list('id_offer', flat=True))
    queryset = Offer.objects.filter(id__in=active_offers)

    if not request.user.is_anonymous:
        queryset = queryset.exclude(user=request.user.id)

    if "type-service" in request.GET:
        if not request.GET.get('type-service') == 'Tout':
            queryset = queryset.filter(
                type_service__icontains=request.GET.get('type-service'))

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

        queryset.filter(end_date__gte=date)

    if "mots-cles" in request.GET:
        mots_cles = request.GET.getlist('mots-cles')[0].split(',')
        queryset = queryset.filter(
            reduce(and_, (Q(description__icontains=mot) for mot in mots_cles)))

    serializer = OfferSerializer(queryset, many=True)
    if not request.user.is_anonymous:
        offers = sort_offers_by_distance(request.user.id, [dict(obj) for obj in serializer.data])
    else:
        offers = serializer.data
    return Response(offers)

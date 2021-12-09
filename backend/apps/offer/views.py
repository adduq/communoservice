import requests
from django.db.models import Q
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view  # Pour utilser annotations

from rest_framework import status
from .models import ActiveOffer, Offer, ReservedOffer, ServiceType, TerminatedOffer
from apps.userinfo.models import UserInfo
from .serializers import ActiveOfferCreationSerializer, ActiveOfferSerializer, OfferSerializer, ReservedOfferCreationSerializer, ReservedOfferSerializer, ServiceTypeSerializer, TerminatedOfferCreationSerializer, TerminatedOfferSerializer

from rest_framework.decorators import api_view

from functools import reduce
from operator import and_
from math import cos, asin, sqrt, pi

PUBLIC_MAPBOX_KEY = "pk.eyJ1IjoidmFuaXR5cHciLCJhIjoiY2t2a2FhcmxmZDNkOTJxcTYybXNkODRoZSJ9.dNeojMWUvXZH-TkiFqTexA"

def sort_offers_by_distance(user_id, offers):

    me = UserInfo.objects.get(user_id=user_id)

    def haversine(lat1, lon1, lat2, lon2):
        p = pi/180
        a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(a))

    def check_distance(offer):
        employe = UserInfo.objects.get(user_id=offer['user'])
        if employe.location_lat == '' or employe.location_lon == None or employe.location_lat == '' or employe.location_lon == None:
            return False
        dist = haversine(float(me.location_lat), float(me.location_lon), float(employe.location_lat), float(employe.location_lon))        
        if dist < float(offer['max_distance']):
            return driving_distance(employe.location_lon, employe.location_lat, offer['max_distance'])
        else:
            return False
    
    def driving_distance(employe_lon, employe_lat, max_distance):
        # if driving distance > offer['max_distance'] then exclude from candidates
        formated_url = "https://api.mapbox.com/directions/v5/mapbox/driving/{0},{1};{2},{3}?access_token={4}".format(me.location_lon, me.location_lat, employe_lon, employe_lat, PUBLIC_MAPBOX_KEY)
        response = requests.get(formated_url)
        data = response.json()
        if data['code'] == 'NoRoute':
            return False
        else:
            return float(data['routes'][0]['distance'])/1000 < float(max_distance)
    
    if me.location_lat != '' and me.location_lat != None and me.location_lon != '' and me.location_lon != None:
        potential_offers = map(check_distance, offers)
        return [d for (d, keep) in zip(offers, potential_offers) if keep]
    else:
        return offers


"""
Permet de supprimer les informations sensibles de la réponse.
"""
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
    Création d'une offre.
    """

    def user_can_create(self, user_id):
        user = UserInfo.objects.get(user_id=user_id)
        return user.profile_is_completed

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if request.data['user'] is not None and request.user.id != request.data['user']:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        if self.user_can_create(request.user.id):
            serializer = OfferSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {'error': 'profile_incomplete'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class OfferDetail(APIView):

    """
    Récupérer une offre selon l'id de l'offre.
    """

    def get_object(self, id_offer):
        try:
            return Offer.objects.get(id=id_offer)
        except Offer.DoesNotExist:
            raise Http404

    def put(self, request, id_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if request.data['user'] is not None and request.user.id != request.data['user']:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        offer = self.get_object(id_offer)
        serializer = OfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceTypes(APIView):
    def get(self, request, format=None):
        service_types = ServiceType.objects.all()
        serializer = ServiceTypeSerializer(service_types, many=True)
        return Response(serializer.data)

# region ActiveOffers


class ActiveOffers(APIView):
    """
    Permet d'avoir les offres actives.
    """

    def get(self, request, format=None):
        offset = request.GET.get('offset')
        if offset is None:
            offset = 0
        else:
            offset = int(offset)

        active_offers = []
        offers = []

        if not request.user.is_anonymous:
            total_active_offers = ActiveOffer.objects.exclude(
                id_user=request.user.id).count()

            active_offers = ActiveOffer.objects.filter(~Q(
                    id_user=request.user.id)).order_by('-id_offer__max_distance').distinct()

            # Permet de faire la bonne requête selon la taille du offset.
            if offset + 5 < total_active_offers:
                active_offers = active_offers[offset:offset+5]
            else:
                active_offers = active_offers[offset:total_active_offers]

            serializer = ActiveOfferSerializer(active_offers, many=True)
            remove_user_infos(serializer)

            for elem in serializer.data:
                offers.append(elem['id_offer'])

            offers = sort_offers_by_distance(
                request.user.id, [dict(obj) for obj in offers])
        else:
            active_offers = ActiveOffer.objects.all().order_by(
                '-id_offer__max_distance').distinct()[offset:offset+5]

            serializer = ActiveOfferSerializer(active_offers, many=True)

            for elem in serializer.data:
                offers.append(elem['id_offer'])

        return Response(offers)

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if request.data['id_user'] is not None and request.user.id != request.data['id_user']:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        serializer = ActiveOfferCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveOffersTotal(APIView):
    """
    Permet d'avoir le total de chaque liste pour les requête de scroll infinie.
    """

    def get(self, request, format=None):
        page = request.GET.get('page')

        if not request.user.is_anonymous:
            if page == 'home':
                active_offers = ActiveOffer.objects.exclude(
                    id_user=request.user.id).count()
            elif page == 'account':
                nbOffer = ActiveOffer.objects.filter(
                    id_user=request.user.id).count()
                nbReserveUser = ReservedOffer.objects.filter(
                    id_user=request.user.id).count()
                nbReserveRecruiter = ReservedOffer.objects.filter(
                    id_recruiter=request.user.id).count()
                nbTerminateUser = TerminatedOffer.objects.filter(
                    id_user=request.user.id).count()
                nbTerminateRecruiter = TerminatedOffer.objects.filter(
                    id_recruiter=request.user.id).count()

                active_offers = {
                    'offerEmployee': nbOffer,
                    'offerReserveUser': nbReserveUser,
                    'offerReserveRecruiter': nbReserveRecruiter,
                    'offerTerminateUser': nbTerminateUser,
                    'offerTerminateRecruiter': nbTerminateRecruiter,
                }
        else:
            active_offers = ActiveOffer.objects.all().count()

        return Response(active_offers)


class ActiveOffersByUser(APIView):
    """
    Permet d'avoir les offres actives par utilisateur.
    """

    def get(self, request, no_user, format=None):
        offset = request.GET.get('offset')
        if offset is None:
            offset = 0
        else:
            offset = int(offset)

        active_offers = ActiveOffer.objects.filter(id_user=no_user)[offset:offset+5]        
        serializer = ActiveOfferSerializer(active_offers, many=True)

        offers = []
        remove_user_infos(serializer)

        for elem in serializer.data:
            elem['id_offer']['id_active_offer'] = elem['id']
            offers.append(elem['id_offer'])

        return Response(offers)


class ActiveOfferWithId(APIView):
    """
    Permet d'avoir une offre active selon son id et l'id de l'utilisateur.
    """

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
        except:
            raise Http404

    def get(self, request, id_active_offer, format=None):
        active_offer = self.get_object(id_active_offer)
        serializer = ActiveOfferCreationSerializer(active_offer)
        return Response(serializer.data)

    def delete(self, request, id_active_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        active_offer = self.get_object(id_active_offer)

        if active_offer.id_user != request.user:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        active_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# endregion

# region ReservedOffers


class ReservedOffers(APIView):
    """
    Permet d'avoir les offres réservées.
    """

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if request.data['id_recruiter'] is not None and request.user.id != request.data['id_recruiter']:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

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
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        offset = request.GET.get('offset')
        if offset is None:
            offset = 0
        else:
            offset = int(offset)

        reserved_offers = ReservedOffer.objects.filter(id_user=no_user)[offset:offset+5]
        serializer = ReservedOfferSerializer(reserved_offers, many=True)
        remove_user_infos(serializer)

        return Response(serializer.data)


class ReservedOffersByRecruiter(APIView):
    """
    Permet d'avoir les offres réservées en tant qu'employeur.
    """

    def get(self, request, no_recruiter, format=None):
        if request.user.is_anonymous or request.user.id != no_recruiter:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        offset = request.GET.get('offset')
        if offset is None:
            offset = 0
        else:
            offset = int(offset)

        reserved_offers = ReservedOffer.objects.filter(
            id_recruiter=no_recruiter)[offset:offset+5]
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
        except:
            raise Http404

    def get(self, request, id_reserved_offer, format=None):
        res = []
        try:            
            reserved_offers = ReservedOffer.objects.filter(
                id_offer=id_reserved_offer)
            serializer = ReservedOfferCreationSerializer(
                reserved_offers, many=True)
            res = serializer.data
        except:
            res = []

        return Response(res)

    def delete(self, request, id_reserved_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        reserved_offer = self.get_object(id_reserved_offer)

        if reserved_offer.id_user != request.user and reserved_offer.id_recruiter != request.user:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        reserved_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id_reserved_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if ((request.data['id_recruiter'] is not None and request.user.id != request.data['id_recruiter']) and
            (request.data['id_user'] is not None and request.user.id != request.data['id_user'])):
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

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

    def post(self, request, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if ((request.data['id_recruiter'] is not None and request.user.id != request.data['id_recruiter']) and
            (request.data['id_user'] is not None and request.user.id != request.data['id_user'])):
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

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
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        offset = request.GET.get('offset')
        if offset is None:
            offset = 0
        else:
            offset = int(offset)

        terminated_offers = TerminatedOffer.objects.filter(id_user=no_user)[offset:offset+5]
        serializer = TerminatedOfferSerializer(terminated_offers, many=True)
        remove_user_infos(serializer)
        return Response(serializer.data)


class TerminatedOffersByRecruiter(APIView):
    """
    Permet d'avoir les offres terminées en tant qu'employeur.
    """

    def get(self, request, no_recruiter, format=None):
        if request.user.is_anonymous or request.user.id != no_recruiter:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        offset = request.GET.get('offset')
        if offset is None:
            offset = 0
        else:
            offset = int(offset)

        terminated_offers = TerminatedOffer.objects.filter(
            id_recruiter=no_recruiter)[offset:offset+5]
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
        except:
            raise Http404

    def delete(self, request, id_terminated_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        terminated_offer = self.get_object(id_terminated_offer)

        if terminated_offer.id_user != request.user and terminated_offer.id_recruiter != request.user:
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        terminated_offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id_terminated_offer, format=None):
        if request.user.is_anonymous:
            return Response('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)

        if ((request.data['id_recruiter'] is not None and request.user.id != request.data['id_recruiter']) and
            (request.data['id_user'] is not None and request.user.id != request.data['id_user'])):
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

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

    # Permet de retirer les offres réservées.
    if request.GET.get('date') is not None:
        reserved_days = list(
            ReservedOffer.objects.filter(reservation_date=request.GET.get('date')).values_list('id_offer', flat=True))
        active_offers_tmp = list(
            ActiveOffer.objects.all().values_list('id_offer', flat=True))

        active_offers = [
            x for x in active_offers_tmp if x not in reserved_days]

    queryset = Offer.objects.filter(id__in=active_offers).order_by('-max_distance').distinct()

    # Exclue les offres de l'utilisateur.
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

        queryset = queryset.filter(Q(end_date__gte=date, start_date__lte=date) |
                                   Q(end_date=None, start_date__lte=date) |
                                   Q(end_date__gte=date, start_date=None) |
                                   Q(end_date=None, start_date=None))

    if "mots-cles" in request.GET:
        mots_cles = request.GET.getlist('mots-cles')[0].split(',')
        queryset = queryset.filter(
            reduce(and_, (Q(description__icontains=mot) for mot in mots_cles)))

    offset = request.GET.get('offset')
    if offset is None:
        offset = 0
    else:
        offset = int(offset)

    queryset = queryset[offset:offset+5]

    serializer = OfferSerializer(queryset, many=True)
    if not request.user.is_anonymous:
        offers = sort_offers_by_distance(request.user.id, [dict(obj) for obj in serializer.data])
    else:
        offers = serializer.data
    return Response(offers)

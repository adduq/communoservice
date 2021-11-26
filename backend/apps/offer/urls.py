from django.urls import path
from apps.offer import views

urlpatterns = [
    path('offers/', views.Offers.as_view(), name="offers"),
    path('offers/<int:id_offer>/', views.OfferDetail.as_view(), name="offers"),

    path('active-offers/', views.ActiveOffers.as_view(), name="active-offers"),
    path('active-offers/<int:id_offer>/<int:no_user>/',
         views.ActiveOfferWithId.as_view()),
    path('active-offers/<int:id_active_offer>/',
         views.ActiveOfferDetail.as_view()),
    path('active-offers/user/<int:no_user>/',
         views.ActiveOffersByUser.as_view()),

    path('reserved-offers/', views.ReservedOffers.as_view()),
    path('reserved-offers/<int:id_reserved_offer>/',
         views.ReservedOfferDetail.as_view()),
    path('reserved-offers/user/<int:no_user>/',
         views.ReservedOffersByUser.as_view()),
    path('reserved-offers/recruiter/<int:no_recruiter>/',
         views.ReservedOffersByRecruiter.as_view()),

    path('terminated-offers/', views.TerminatedOffers.as_view()),
    path('terminated-offers/<int:id_terminated_offer>/',
         views.TerminatedOfferDetail.as_view()),
    path('terminated-offers/user/<int:no_user>/',
         views.TerminatedOffersByUser.as_view()),
    path('terminated-offers/recruiter/<int:no_recruiter>/',
         views.TerminatedOffersByRecruiter.as_view()),

    # path('offers/user/<int:no_user>/', views.UserOffers.as_view()),
    path('active-offers/search', views.search),

    path('service-types/', views.ServiceTypes.as_view())
]

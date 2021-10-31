from django.urls import path, include

from apps.offer import views

urlpatterns = [
    path('offers/', views.Offers.as_view()),
    path('offers/<int:no_offer>/', views.OfferDetail.as_view()),
    path('active-offers/', views.ActiveOffers.as_view()),
    path('active-offers/<int:id_active_offer>/',
         views.ActiveOfferDetail.as_view()),
    path('reserved-offers/', views.ReservedOffers.as_view()),
    path('reserved-offers/<int:id_reserved_offer>/',
         views.ReservedOfferDetail.as_view()),
    path('terminated-offers/', views.TerminatedOffers.as_view()),
    path('terminated-offers/<int:id_terminated_offer>/',
         views.TerminatedOfferDetail.as_view()),
    path('offers/user/<int:no_user>/', views.UserOffers.as_view()),
    path('offers/search', views.search)
]

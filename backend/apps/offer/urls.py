from django.urls import path, include

from offer import views

rlpatterns = [
    path('offers/', views.OfferList.as_view()),
    path('offers/<int:no_offer>/', views.OfferDetail.as_view()),
    path('<int:no_user>/', views.UserOffers.as_view()),
]

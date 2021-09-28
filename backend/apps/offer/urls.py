from django.urls import path, include

from offer import views

urlpatterns = [
    path('offers/', views.Offers.as_view()),
    path('offers/<int:no_offer>/', views.OfferDetail.as_view()),
    path('<int:no_user>/', views.UserOffers.as_view()),
    path('offers/search', views.search)
]

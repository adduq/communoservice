from django.urls import path, include

from userinfo import views

urlpatterns = [
    path('userinfo/<int:user_id>/', views.UserInfoDetail.as_view()),
]

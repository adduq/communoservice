from django.urls import path, include

from apps.userinfo import views

urlpatterns = [
    path('userinfo/<int:user_id>/', views.UserInfoDetail.as_view()),
    path('userinfo/me/', views.MyUserInfo.as_view()),
]

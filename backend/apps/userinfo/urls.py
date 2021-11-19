from django.urls import path, include

from apps.userinfo import views

urlpatterns = [
    path('userinfo/<int:user_id>/', views.UserInfoDetail.as_view()),
    path('userinfo/me/', views.MyUserInfo.as_view()),
    path('userinfo/me/update/', views.UpdateUserInfo.as_view()),
    path('userinfo/<int:user_id>/update-employee/<int:recruiter_id>/',
         views.updateAvgDataEmployee.as_view()),
    path('userinfo/<int:recruiter_id>/update-recruiter/<int:user_id>/',
         views.updateAvgDataRecruiter.as_view()),
]

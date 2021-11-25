from django.urls import path, include

from apps.userinfo import views

urlpatterns = [
    path('userinfo/<int:user_id>/', views.UserInfoDetail.as_view(), name="userinfo"),
    path('userinfo/me/', views.MyUserInfo.as_view()),
    path('userinfo/me/update/', views.UpdateUserInfo.as_view()),
    path('userinfo/me/profile-image/', views.UpdateUserProfileImage.as_view()),
    path('userinfo/me/status/', views.UserStatus.as_view()),
    path('userinfo/<int:user_id>/update-employee/<int:recruiter_id>/',
         views.UpdateEmployeeRating.as_view()),
    path('userinfo/<int:recruiter_id>/update-recruiter/<int:user_id>/',
         views.UpdateRecruiterRating.as_view()),
]

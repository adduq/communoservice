from django.urls import path

from apps.userinfo import views

urlpatterns = [
    path('userinfo/<int:user_id>/', views.UserInfoDetail.as_view(), name="userinfo"),
    path('userinfo/me/', views.MyUserInfo.as_view(), name="userinfo/me/"),
    path('userinfo/me/update/', views.UpdateUserInfo.as_view(), name="userinfo/me/update/"),
    path('userinfo/me/profile-image/', views.UpdateUserProfileImage.as_view()),
    path('userinfo/me/status/', views.UserStatus.as_view(), name="userinfo/me/status/"),
    path('userinfo/<int:user_id>/update-employee/<int:recruiter_id>/',
         views.UpdateEmployeeRating.as_view(), name="userinfo/<user_id>/update-employee/<recruiter_id>/"),
    path('userinfo/<int:recruiter_id>/update-recruiter/<int:user_id>/',
         views.UpdateRecruiterRating.as_view()),
]

"""
!NOTE: Version généré auto
"""
# from django.urls import path
# from django.contrib import admin
# from django.contrib.auth import logout

# from django.conf.urls import include

# from config.api import api


# urlpatterns = [
#     path('admin/', admin.site.urls, name='admin'),
#     path('logout/', logout, {'next_page': '/'}, name='logout'),

#     path('api/', include(api.urls)),
#     path('api-auth/', include('rest_framework.urls',
# namespace='rest_framework')),

# ]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('api/v1/', include('offer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

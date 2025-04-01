from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('v1/api/' , include('core_apps.musicapp.urls') , name='music api')
]

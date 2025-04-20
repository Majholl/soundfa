from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('v1/api/' , include('core_apps.musicapp.urls') , name='Music api\'s'),
    path('api/auth/', include('core_apps.user.urls'), name='Authentication api\'s')
    ] 




urlpatterns + static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)


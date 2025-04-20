from django.urls import path 

from .views import user_views


urlpatterns = [
    path('register/', user_views.register_user, name='Register user'),
    path('login/', user_views.login_user, name='Login user'),
    path('refresh/', user_views.refresh_token, name='Refresh user token'),
    path('logout/', user_views.logout_user, name='Logout user')
]
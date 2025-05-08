from django.urls import path 

from .views import user_views


urlpatterns = [
    path('register/', user_views.register_user, name='Register user'),
    path('otp/<str:uuid>/<str:otp>/', user_views.verify_otp, name='Verify_otp'),
    path('login/', user_views.login_user, name='Login user'),
    path('refresh/', user_views.refresh_token, name='Refresh user token'),
    path('getme/', user_views.get_me_user, name='Get me'),
    path('user/update/', user_views.update_user, name='Update user info'),
    path('reset-password/', user_views.reset_password, name='Reset password'),
    path('reset-password/confirmation/', user_views.reset_password_confirm, name='Reset password'),
    path('logout/', user_views.logout_user, name='Logout user')
]
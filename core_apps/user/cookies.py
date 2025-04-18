from django.conf import settings


def set_auth_cookies(response, access_token, refresh_token=None,) :
    access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
    
    cookie_settings = {
        'path' : settings.COOKIE_PATH,
        'secure' : settings.COOKIE_SECURE,
        'httponly' : settings.COOKIE_HTTPONLY,
        'samesite' : settings.COOKIE_SAMESITE,
        'max_age' : access_token_lifetime}
    response.set_cookie('access', access_token, **cookie_settings)
    
    if refresh_token:
        refresh_token_litetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
        refresh_token_settings = cookie_settings.copy()
        refresh_token_settings['max_age'] = refresh_token_litetime 
        response.set_cookie('refresh', refresh_token, **refresh_token_settings)
        
        
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings['httponly'] = False
    response.set_cookie('logged_in', 'true', **logged_in_cookie_settings)        
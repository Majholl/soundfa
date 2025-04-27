from rest_framework.request import Request
from rest_framework_simplejwt.authentication import AuthUser, JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import Token
from django.conf import settings
from loguru import logger



class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        
        header = self.get_header(request)
        raw_token = None
        
        if header is not None:
            raw_token = self.get_raw_token(header)
        elif settings.COOKIE_NAME in request.COOKIES:
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)
            
        if raw_token is not None:
            try:
                validate_token = self.get_validated_token(raw_token)
                return self.get_user(validate_token), validate_token
            except TokenError as err:
                logger.error(f'Token validation error {str(err)}')
                
        return None
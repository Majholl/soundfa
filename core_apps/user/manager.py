from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate_email_address(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
     
    
    
class customUserManager(UserManager):
    
    def _create_user(self, email, password, **extra_fields):
        
        if not email :
            raise ValueError('An email address must be provided.')
        
        if not password:
            raise ValueError('A password must be provided.')
        
        email = self.normalize_email(email)
        validate_email_address(email=email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('usertype' , 'superadmin')
        return self._create_user(email, password, **extra_fields)
    
    
    def create_admin(self, email, password, **extra_fields):
        extra_fields.setdefault('usertype' , 'admin')
        return self._create_user(email, password, **extra_fields)
    
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
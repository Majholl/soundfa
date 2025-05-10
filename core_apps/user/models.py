from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models
from time import time
from os import path
from loguru import logger


from .manager import customUserManager
from ..musicapp.models.playlists import PlaylistModel


# -------------------------------------------------------------------
# Users Model

# This model extends Django's AbstractUser to add custom fields and logic:
# - User types: normal user, admin, superadmin (via choices)
# - Account status: active, deactive, locked (via choices)
# - Custom profile image upload path using a timestamped filename
# - Many-to-many relationship with playlists
# - Password reset system with code, expiration time, and attempt counter
# - Timestamp fields for account creation and last update

# -------------------------------------------------------------------



def profile_file_cover(instance ,filename):
    try:
        
        split_name = path.splitext(filename)
        file_name = f'{instance.username}_{int(time())}{split_name[-1]}'
        return path.join('users', file_name)
    
    except Exception as err:
        logger.info(f'Error saving user profile image name | user-id : {instance.pk} | {str(err)}')
        print(f'Error saving user profile image name | user-id : {instance.pk} | {str(err)}')
          
          
          
class Users(AbstractUser):
    
    class UserType(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        SUPERADMIN = 'superadmin', 'Superadmin'
    
    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DEACTIVE = 'deactive', 'Deactive'
        LOCKED = 'locked', 'Locked'


  
        
    email = models.EmailField('Email address', db_index=True, unique=True)
    playlists = models.ManyToManyField(verbose_name='Playlists', to=PlaylistModel, blank=True, related_name='playlists_users')
    
    profile = models.ImageField('User profile', upload_to=profile_file_cover, blank=True)
    usertype = models.CharField('User type', max_length=10, choices=UserType.choices, default=UserType.USER)
    
    account_status = models.CharField('Account status', max_length=8, choices=AccountStatus.choices, default=AccountStatus.DEACTIVE)
    is_active = models.BooleanField('Account activation', default=0)
    
    otp = models.CharField('One time password', max_length=6, null=True)
    otp_expire_time = models.DateTimeField('One time password expiration', null=True, blank=True)
    otp_attempt = models.IntegerField('One time password attempt', default=0)
    
    reset_password = models.CharField('Reset password', max_length=6, null=True)
    reset_password_expire_time = models.DateTimeField('Reset password expiration time', null=True, blank=True)
    reset_password_attempt = models.IntegerField('Reset password attempt', default=0)
    
    created_at = models.DateTimeField('Creatation datetime', auto_now_add=True)
    updated_at = models.DateTimeField('Last modification', auto_now=True)
    
    
    date_joined = None
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']
    
    objects = customUserManager()
    
    class Meta:
        verbose_name = 'User'
        db_table = 'users'
        ordering = ['-created_at']
        
        
    def set_otp(self, code:str):
        self.otp = code
        self.otp_expire_time = timezone.now() + settings.OTP_EXPIRE_TIME
        self.save()    
      
        
    @property
    def validate_otp_expiration(self):
        return (timezone.now() - self.otp_expire_time) <= settings.OTP_EXPIRE_TIME
   
   
   
        
    @property
    def otp_attempt_count(self):
        if self.otp_attempt <4:
            self.otp_attempt +=1 
        if self.otp_attempt >= 3 :
            self.account_status = Users.AccountStatus.LOCKED
        self.save()        
        
        
    @property
    def otp_code_expiration(self):
        self.otp = None
        self.otp_expire_time = None
        self.otp_attempt = 0 
        self.save()    
        
        
        
        
        
        
    def set_resest_password(self,  code:str):
        self.reset_password = code
        self.reset_password_expire_time = timezone.now() + settings.RESET_PASSWORD_EXPIRE_TIME
        self.save()
        
        
    @property
    def validate_reset_password_code_expiration(self):
        return (timezone.now() - self.reset_password_expire_time) <= settings.RESET_PASSWORD_EXPIRE_TIME

    @property
    def reset_password_code_expiration(self):
        self.reset_password = None
        self.reset_password_expire_time = None
        self.reset_password_attempt = 0 
        self.save()
        
    @property
    def reset_password_attempt_count(self):
        if self.reset_password_attempt <4:
            self.reset_password_attempt +=1 
        if self.reset_password_attempt >= 3 :
            self.account_status = Users.AccountStatus.LOCKED
        self.save()
          
        
          
    def get_full_name(self):
        return super().get_full_name()
        
    
    def __str__(self):
        return f'{self.email} - {self.usertype}'

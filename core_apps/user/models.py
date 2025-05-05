from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models
from os import path
from time import time

from .manager import customUserManager
from ..musicapp.models.playlists import PlaylistModel

"""

    -This file is include all fields for the users 
    #- This model is using for authentication

"""
def profile_file_cover(instance ,filename):
    try:
        splitedName = path.splitext(filename)
        fileName = f'{instance.username}_{instance.updated_at}{splitedName[-1]}'
        return path.join('users', fileName)
    except Exception as err:
        print(f'Error while editting users profile image name : error {str(err)}')


def nowTimeStamp():
    return int(time())


class Users(AbstractUser):
    class userType(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        SUPERADMIN = 'superadmin', 'Superadmin'
    
    class AccountStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        LOCKED = 'locked', 'Locked'
        
    email = models.EmailField(db_index=True, unique=True)
    playlists = models.ManyToManyField(to=PlaylistModel, blank=True, related_name='playlists_users')
    
    profile = models.ImageField(upload_to=profile_file_cover, blank=True)
    usertype = models.CharField(max_length=10, choices=userType.choices, default=userType.USER)
    
    account_status = models.CharField(max_length=8, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    
    reset_password = models.CharField(max_length=6, null=True)
    reset_password_expire_time = models.DateTimeField(null=True, blank=True)
    reset_password_attempt = models.IntegerField(default=0)
    
    created_at = models.BigIntegerField(default=nowTimeStamp)
    updated_at = models.BigIntegerField(default=nowTimeStamp)
    
    
    date_joined = None
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']
    
    objects = customUserManager()
    
    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.email} - {self.usertype}'
    
    def set_resest_password(self,  code:str):
        self.reset_password = code
        self.reset_password_expire_time = timezone.now() + settings.RESET_PASSWORD_EXPIRE_TIME
        self.save()
        
    def get_full_name(self):
        return super().get_full_name()
    
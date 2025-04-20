from django.contrib.auth.models import AbstractUser
from django.db import models
from time import time


from .manager import customUserManager
from ..musicapp.models.playlists import PlaylistModel

"""

    -This file is include all fields for the users 
    #- This model is using for authentication

"""

def nowTimeStamp():
    return int(time())


class Users(AbstractUser):
    class userType(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        SUPERADMIN = 'superadmin', 'Superadmin'
        
    email = models.EmailField(db_index=True, unique=True)
    playlists = models.ManyToManyField(to=PlaylistModel, blank=True)
    usertype = models.CharField(max_length=10, choices=userType.choices, default=userType.USER)
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
    
    
    
    